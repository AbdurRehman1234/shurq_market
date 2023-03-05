from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Customize django User functionality
    """
    pass

class Script(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id: {self.id} name: {self.name}"

class MarketChart(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    chart_img = models.TextField(max_length=1000, null=True, blank=True)
    # chart_img = models.ImageField(upload_to='images/', blank=True, null=True)
