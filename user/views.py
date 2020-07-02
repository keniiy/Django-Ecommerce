from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from product.models import Category, Comment
from user.models import UserProfile
from user.forms import SignUpForm
from user.forms import ProfileUpdateForm, UserUpdateForm
from order.models import Order, OrderProduct
from home.models import FAQ


@login_required(login_url='/login') # Check login
def index(request):
    category = Category.objects.all()
    current_user = request.user # access user session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'profile': profile
    }
    return render(request, 'user_profile.html', context)

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
    #return an invalid login error messae


    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'login_form.html',context)

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed signup
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
    form = SignUpForm
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form
    }
    return render(request, 'signup_form.html',context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() # completed signup
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password as been successfully Changed!")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'pls correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'category': category,
            'form': form
        }
        return render(request, 'user_password.html', context)

@login_required(login_url='/login')
def user_order(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders
    }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login')
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'order_product': order_product
    }
    return render(request, 'user_order_products.html', context)


def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    current_user = request.user  # access user session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
        'profile': profile
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Your Comment Has Been Deleted..')
    return HttpResponseRedirect('/user/comments')

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all()
    context = {
        'category': category,
        'faq': faq
    }
    return render(request, 'faq.html', context)