from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import Farmer

admin.site.register(Farmer, auth_admin.UserAdmin)