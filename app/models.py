import random
import string

from django.db import models

get_rand_string = lambda x:''.join(random.choice(string.ascii_lowercase) for _ in range(x))


class Products(models.Model):
    product_name = models.CharField(max_length=255, unique=True)

class Store(models.Model):
    store_name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('Products')

class Discount(models.Model):
    products = models.ManyToManyField('Products')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class StoreDiscount(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
