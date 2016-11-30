from django.contrib import admin

# Register your models here.
from .models import Book, InternetDongle, TransactionRecord

admin.site.register(Book)
admin.site.register(InternetDongle)
admin.site.register(TransactionRecord)