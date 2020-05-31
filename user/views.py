from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from product.models import Category


def index(request):
    return HttpResponse("User App")

def login_form(request):
    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'login_form.html',context)

def signup_form(request):
    return HttpResponse("sign form")