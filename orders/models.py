from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=20)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_number

    @property
    def order_total(self):
        total = 0
        for item in self.order_items.all():
            total += item.discounted_price

        return total



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount_percentage = models.FloatField(default=0)


    def __str__(self):
        return self.product.name

    @property
    def sub_total(self):
        return int(self.product.price) * int(self.quantity)


    @property
    def discounted_price(self):
        return self.sub_total * (1 - self.discount_percentage*0.01)