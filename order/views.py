from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from order.models import ShopCart, ShopCartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category, Product


# Create your views here.
from user.models import UserProfile
from order.models import OrderForm, Order, OrderProduct



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
    current_user = request.user #access user session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
    }
    return render(request, 'shopcart.html', context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Items as as been sucessfully deleted from shopcart")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user  # access user session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST': #if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.Items())
        if form.is_valid():
            # send credit information to bank and get result if bank return payment information
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper() #random code
            data.code = ordercode
            data.save()

            #Then we move Shopcart items to order Products items
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id #Order
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # Remove quantity  of sold product from amount of product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            # then we clear and delete shop cart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank You")
            return render(request, 'order_completed.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    form = Order()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'order_form.html', context)