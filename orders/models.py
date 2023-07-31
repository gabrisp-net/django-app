from django.db import models
from users.models import User
import datetime

# Create your models here.
class Order(models.Model):
    uid = models.CharField(max_length=8, unique=True, blank=True)
    payment_intent = models.CharField(max_length=255, blank=False)
    stripe = models.JSONField()
    cart = models.JSONField()
    billing_address = models.JSONField()
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today())