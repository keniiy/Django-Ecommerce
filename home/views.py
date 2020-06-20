from django.shortcuts import render
from django.http import HttpResponse
from home.models import Setting
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from home.models import ContactForm, ContactMessages
from product.models import Category, Product, Images
from home.forms import SearchForm
from django.db.models import Q
import json
from product.models import Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    products_latest = Product.objects.all().order_by('-id')[:4]
    products_picked = Product.objects.all().order_by('?')[:4]
    prdouct_banner1 = Product.objects.all().order_by('?')[:1]
    prdouct_banner2 = Product.objects.all().order_by('?')[:4]
    new_arrival = list(Product.objects.filter(new_arrival=True).order_by('id'))[0:10]
    products_all = list(Product.objects.all().order_by('id'))[0:10]
    products_men = list(Product.objects.filter(men_home=True).order_by('id'))[0:10]
    products_women = list(Product.objects.filter(women_home=True).order_by('id'))[0:10]
    products_discount = list(Product.objects.filter(discount_home=True).order_by('id'))[0:10]
    products_kids = list(Product.objects.filter(kids_home=True).order_by('id'))[0:10]

    page = "home"
    context = {
        'setting': setting,
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        'prdouct_banner1': prdouct_banner1,
        'prdouct_banner2': prdouct_banner2,
        'new_arrival': new_arrival,
        'products_all': products_all,
        'products_men': products_men,
        'products_women': products_women,
        'products_discount': products_discount,
        'products_kids': products_kids,
        'category': category
        
    }
    return render(request, 'homepage.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {
        'setting': setting
    }
    return render(request, 'about.html', context)

def contactus(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = ContactMessages()#create relation with model
            data.name =  form.cleaned_data['name']# get from input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.telephone = form.cleaned_data['telephone']
            data.message = form.cleaned_data['message']
            data.ip_address = request.META['REMOTE_ADDR']
            data.save() # save data to table
            messages.success(request, "Your message has been sent. Thank You for your Contacting us we would get back to you shortly")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {
        'setting': setting,
        'form': form
    }
    return render(request, 'contact.html',context)

def category_products(request,id,slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    catdata = Category.objects.get(pk=id)
    context = {
        'products': products,
        'category': category,
        'catdata': catdata
    }
    return render(request, 'category_products.html', context)


def search(request):
    querysets = Product.objects.all()
    query = request.GET.get('q')
    if query:
        querysets = querysets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) 
        ).distinct()
    else:
        querysets = Product.objects.all()
    

    category = Category.objects.all()
    context = {
        'querysets': querysets,
        'category': category
    }
    return render(request, 'search_products.html', context)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments
    }
    return render(request, 'product-details.html', context)