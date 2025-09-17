from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def ninja_page(request):
    return render(request, "index_ninja.html")

def fastapi_page(request):
    return render(request, "index_fastapi.html")
