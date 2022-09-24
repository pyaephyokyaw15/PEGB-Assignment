from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from accounts.models import Account, CustomerCategory
from drf_extra_fields.fields import Base64ImageField
from products.models import Product, Category
from accounts.models import Account, CustomerCategory


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Invalid email or password.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        # print('Attrs', attrs)
        attrs['user'] = user  # add user to serializer response
        # print(attrs)
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'password', 'first_name', 'last_name']
        # override error message
        extra_kwargs = {
            "email": {"error_messages": {"required": "email is required"}},
            "password": {"error_messages": {"required": "password is required"}},
        }

    # https://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
    def create(self, validated_data):
        user = Account(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])  # hash password
        customer_category = CustomerCategory.objects.filter(name='Bronze').first()
        user.customer_category = customer_category
        user.save()
        return user


class CustomerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCategory
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(read_only=True, slug_field="name")
    customer_category = CustomerCategorySerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'department', 'customer_category']


class CategorySerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Category
        fields = ['id', 'name', 'department', 'discount_percentage']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'category', 'image']
        read_only_fields = ['id', 'category']  # show only on GET request

    def create(self, validated_data):  # override the create method
        print(validated_data)
        request = self.context.get('request')

        validated_data['category'] = request.user.department.category  # assign the product category according to the staff department
        print(validated_data)
        obj = super().create(validated_data)
        return obj