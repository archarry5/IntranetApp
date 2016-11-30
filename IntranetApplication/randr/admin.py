from django.contrib import admin

# Register your models here.
from .models import Associate, Recognition

admin.site.register(Associate)
admin.site.register(Recognition)