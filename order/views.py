from django.shortcuts import render, redirect
from django.http import HttpResponse
from order.models import ShopCart, ShopCartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category


# Create your views here.
def index(request):
    return HttpResponse("order page")

@login_required(login_url='/login') #check if user is logged in
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user #acess user session information

    checkproduct = ShopCart.objects.filter(product_id=id) #check product in shop cart
    if checkproduct:
        control = 1 #the product is in the cart 
    else:
        control = 2 #The product is not in the cart
    
    if request.method == 'POST': #if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1: #update shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else :#insert to shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Your product as been added to your shopping cart")
        return HttpResponseRedirect(url)
    else: #if there is no post
        if control == 1: #if there is no post
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1 
            data.save()
        else: #insert to shop cart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to cart")
        return HttpResponseRedirect(url)

def shopcart(request,):
    category = Category.objects.all()
    current_user = request.user #acess user session information
    shopcart = ShopCart.objects.filter(user=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    context = {
        'category': category,
        'shopcart': shopcart,
        'total': total,
    }
    return render(request, 'shopcart.html', context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Items as as been sucessfully deleted from shopcart")
    return HttpResponseRedirect("/shopcart")