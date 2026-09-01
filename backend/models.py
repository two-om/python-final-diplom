from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_infos')
    external_id = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='product_infos')

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

