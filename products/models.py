from django.db import models
from accounts.models import Department


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    discount_percentage = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/", null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


