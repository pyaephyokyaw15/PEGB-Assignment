from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomAuthTokenSerializer, UserRegisterSerializer, ProductSerializer, \
    UserSerializer, CartSerializer, CartItemSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions, viewsets
from products.models import Product
from accounts.models import Account
from cart.models import Cart, CartItem
from .permissions import DepartmentStaffOnly

# Create your views here.
class TokenView(ObtainAuthToken):
    # POST api/v1/auth/token/
    serializer_class = CustomAuthTokenSerializer


    # generate token
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            # "user": UserInfoSerializer(user).data,
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
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            # "user": UserInfoSerializer(user).data,
            "token": token.key
        })


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [DepartmentStaffOnly]


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