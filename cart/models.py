from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, related_name="user_cart", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def total_price(self):
        return sum([item.sub_total for item in self.cart_items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def sub_total(self):
        return int(self.product.price) * int(self.quantity)