from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomAuthTokenSerializer, UserRegisterSerializer, ProductSerializer, \
    UserSerializer, CartSerializer, CartItemSerializer, CartItemCreateSerializer, \
    OrderSerializer, OrderDetailSerializer, \
    OrderItemSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from products.models import Product
from accounts.models import Account, CustomerCategory
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from .permissions import DepartmentStaffOnly, DepartmentStaffOnly2
from rest_framework import permissions
from accounts.views import send_account_activation_email
from .renderers import CustomApiRenderer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class TokenView(ObtainAuthToken):
    # POST api/v1/auth/token/
    serializer_class = CustomAuthTokenSerializer
    renderer_classes = [CustomApiRenderer]

    # generate token
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })

    def delete(self, request):
        request.user.auth_token.delete()  # simply delete the token to force a login
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        # dynamically change the permission classes according to the request METHOD.

        # To delete token , the user must be authenticated(must have token).
        if self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class UserRegisterAPIView(generics.GenericAPIView):
    # POST api/v1/auth/register/
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        print('Request Data', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = serializer.save()
        print(user)
        print(user.password)

        # create token and return this token
        created = Token.objects.get_or_create(user=user)
        send_account_activation_email(user, request)

        return Response({
            "email": "Account Activation Email is sent."
        })


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [DepartmentStaffOnly]


class StaffProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [DepartmentStaffOnly2]

    def get_queryset(self):
        """Filter the default query_set according to the request parameter"""
        queryset = self.queryset.filter(category=self.request.user.department.category)
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            cart = Cart.objects.create()

        return Response({"cart_id": cart.id}, status=status.HTTP_201_CREATED)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action in ['create', 'update']:
            return CartItemCreateSerializer
        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        """Filter the default query_set according to the request parameter"""
        queryset = self.queryset.filter(customer=self.request.user)
        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        order = Order.objects.create(customer=self.request.user)
        order.save()
        order.order_number = f'S-{order.id:06d}'
        order.save()

        cart = self.request.user.user_cart
        for item in cart.cart_items.all():
            item.product.stock -= 1
            item.product.save()
            order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            order_item.discount_percentage = self.request.user.customer_category.discount_percentage + item.product.category.discount_percentage
            order_item.save()

        CartItem.objects.filter(cart=cart).delete()
        no_orders = Order.objects.filter(customer=request.user).count()

        # find the customer_category according to the user's no of orders
        customer_category = CustomerCategory.objects.filter(minimum_order__lte=no_orders).last()

        # update customer category according to the user's no of orders
        request.user.customer_category = customer_category
        request.user.save()
        return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()