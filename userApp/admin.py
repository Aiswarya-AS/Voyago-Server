from django.contrib import admin
from .models import User, Destination, DestinationImage, Guide, Rating
# Register your models here.
admin.site.register(User)
admin.site.register(Destination)
admin.site.register(DestinationImage)
admin.site.register(Guide)
admin.site.register(Rating)
