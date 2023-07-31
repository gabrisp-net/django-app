from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(blank=False)
    content = RichTextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
