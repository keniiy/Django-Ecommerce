from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from product.models import Category
from user.models import UserProfile
from user.forms import SignUpForm


def index(request):
    return HttpResponse("User App")

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, "Login Error, Incorrect Username Or Password!!")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'login_form.html',context)

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    form = SignUpForm
    category = Category.objects.all()
    context = {
        'category':category,
        'form':form
    }
    return render(request, 'signup_form.html',context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')
