from django.shortcuts import render

# Create your views here.
def index(request):
    import os
    return render(request, 'index.html', locals())
