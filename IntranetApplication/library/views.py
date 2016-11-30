from django.shortcuts import render
from django.views.generic import ListView
from .models import Book

# Create your views here.
def index(request):
    import os
    return render(request, 'index.html', locals())

class BooksView(ListView):
	model = Book