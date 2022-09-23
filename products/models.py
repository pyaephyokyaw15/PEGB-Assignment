from django.db import models
from accounts.models import Department


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.FloatField(default=0)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        return self.price - (self.price*self.discount*0.01)
