from django.contrib import admin
from .models import User, Coordinates, Business, Reviews

# Register your models here.

admin.site.register(User)
admin.site.register(Coordinates)
admin.site.register(Business)
admin.site.register(Reviews)
