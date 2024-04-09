# authentication/admin.py

from django.contrib import admin
from .models import Ride, Driver

admin.site.register(Ride)
admin.site.register(Driver)
