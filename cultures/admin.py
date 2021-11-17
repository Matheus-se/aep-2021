from django.contrib import admin

from .models import Culture, UserCultures

admin.site.register(Culture)
admin.site.register(UserCultures)