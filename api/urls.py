from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
app_name = 'api'


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('carts', views.CartViewSet)
router.register('cart_items', views.CartItemViewSet)
router.register('orders', views.OrderViewSet)
router.register('order_items', views.OrderItemViewSet)


urlpatterns = [
    # starts with api/v1/
    path('', include(router.urls)),
    path('auth/token/', views.TokenView.as_view(), name='token'),
    path('auth/register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('accounts/', views.AccountListView.as_view(), name='accounts'),
    path('staff-products/', views.StaffProductListView.as_view(), name='staff-products')
]
