from django.db import models

from products.models import Product

# Create your models here.
visibility = (
    (0,'public'),
    (1, 'membership'),
)
type = (
    (0, 'product'),
    (1, 'custom'),
    (2,'video'),
)


class Membership(models.Model):
    title = models.CharField(blank=False, max_length=155)
    billing = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=True)
    id_stripe = models.CharField(unique=False, blank=True, max_length=100)
    price = models.FloatField(blank=False)


class ProductMembership(models.Model):
    visibility = models.IntegerField(choices=visibility)
    preview = models.ImageField(upload_to='media/members/', blank=True)
    product_id = models.ForeignKey(Product,default=None, on_delete=models.CASCADE)

class VideoMembership(models.Model):
    visibility = models.IntegerField(choices=visibility)
    url = models.URLField(blank=False)
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    preview = models.ImageField(upload_to='media/members/', blank=True)

class ItemMembership(models.Model):
    visibility = models.IntegerField(choices=visibility)
    preview = models.ImageField(upload_to='media/members/', blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to="downloads/", blank=False)
    other = models.JSONField()
    slug = models.SlugField(unique=True)

