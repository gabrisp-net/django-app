from certifi import where
from django.db import models
from django.utils.html import mark_safe
from orders.models import Order
# Create your models here.

fileChoices = (
    ('video','video'),
    ('image', 'image'),
)
class ProductImage(models.Model):
    product = models.ForeignKey('Product',default=None, on_delete=models.CASCADE)
    url = models.FileField(blank=False)
    alt = models.CharField(max_length=255)
    type = models.CharField(max_length=5, choices=fileChoices, default='image')
    def generate_filename(self, filename):
        return self.get_storage(filename).generate_filename(filename)


class ProductSpecs(models.Model):
    product = models.ForeignKey('Product',default=None, on_delete=models.CASCADE)
    key = models.CharField(max_length=80, blank=True)
    value = models.CharField(max_length=80, blank=True)

class ProductVariation(models.Model):
    product = models.ForeignKey('Product',default=None, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=255)
    price = models.FloatField(blank=False)
    stock = models.IntegerField(blank=True)


class Product(models.Model):
    title = models.CharField(blank=False, max_length=255)
    line = models.CharField(max_length=255, blank=True)
    price = models.FloatField(blank=False)
    published = models.BooleanField(default=False)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    stock = models.IntegerField(blank=True)
    tags = models.ManyToManyField(
        "ProductTag",
        related_name='tags',
        blank=True
    )
    color = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="downloads/", blank=True)
    comingsoon = models.BooleanField(default=False)
    date = models.DateField(blank=True)
    stock = models.IntegerField(blank=True)
    def __str__(self):
        return f"{self.title}"
    def preview(self):
        images = ProductImage.objects.filter(product=self.pk)
        return mark_safe('<img style="object-fit: cover;" src="https://static.gabrisp.net/media/{}" width="300" height="auto" />'.format(images[0].url))
    def ppu(self):
        return mark_safe('{} EURO'. format(self.price))



class ProductDowload(models.Model):
    uid = models.CharField(max_length=20, null=True, blank=True, unique=True)
    product_id = models.ForeignKey('Product',default=None, on_delete=models.CASCADE)
    left = models.IntegerField(default=3, blank=False)
    order = models.ForeignKey(Order,default=None, on_delete=models.CASCADE)



class ProductTag(models.Model):
    name = models.CharField(default=None, max_length=30, blank=False)
    def __str__(self):
        return self.name