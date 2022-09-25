from django.db import models
from accounts.models import Department


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    discount_percentage = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    stock = models.IntegerField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


