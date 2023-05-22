from django.db import models
from userApp.models import User, Guide
# Create your models here.


class AdminWallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    guide_id = models.ForeignKey(Guide, on_delete=models.DO_NOTHING)
    guide_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)
    amount = models.IntegerField()
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)