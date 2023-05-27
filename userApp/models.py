from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class User(models.Model):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    # username = models.CharField(max_length=250)
    email = models.EmailField()
    password = models.CharField(max_length=250)
    phone = models.BigIntegerField()
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    profile_pic = CloudinaryField(
        "user", null=True, default='user/download.jpeg')
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)


class Destination(models.Model):
    country = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    short_desc = models.TextField(max_length=300)
    description = models.TextField(max_length=700)
    thumbnail = CloudinaryField("destination", null=True)
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)


class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="destination")
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)


class Guide(models.Model):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    email = models.EmailField()
    country = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    phone = models.BigIntegerField()
    place = models.CharField(max_length=250)
    pincode = models.IntegerField()
    password = models.CharField(max_length=250)
    pricing = models.IntegerField(null=True, default=100)
    languages_known = models.CharField(max_length=500)
    is_accepted = models.BooleanField(default=False, null=True)
    is_blocked = models.BooleanField(default=False, null=True)
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField("guide", null=True)
    dates = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    video = models.FileField(
        "Video",
        upload_to="videos/",
        null=True,
        blank=True,
        storage=VideoMediaCloudinaryStorage(),
    )
    description = models.CharField(max_length=1000, null=True)


class Request(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    guide_name = models.CharField(max_length=200)
    guide_place = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    total_peoples = models.IntegerField()
    total_amount = models.IntegerField(null=True)
    status = models.CharField(max_length=200, default="Requested")
    price = models.IntegerField()
    location = models.CharField(max_length=2100, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    guide_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    state = models.CharField(max_length=200, default="Tokyo")
    country = models.CharField(max_length=200, default="Japan")
    date = models.DateField()
    time = models.TimeField()
    total_peoples = models.IntegerField()
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_mode = models.CharField()
    transaction_id = models.CharField()
    journey_status = models.CharField(max_length=200, default="pending")
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default="Paid")
    guide_withdraw_status = models.BooleanField(default=False)
    total_amount = models.IntegerField()


class Rating(models.Model):
    guide_id = models.ForeignKey(Guide, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_name = models.CharField(max_length=200, null=True)
    comment = models.TextField(null=True)
    rating = models.IntegerField(default=1)
    is_updated = models.DateTimeField(auto_now=True)
    is_created = models.DateTimeField(auto_now_add=True)


class UserWallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class GuideWallet(models.Model):
    guide_id = models.ForeignKey(Guide, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
