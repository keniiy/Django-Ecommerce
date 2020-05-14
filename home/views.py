from django.shortcuts import render
from django.http import HttpResponse
from home.models import Setting
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from home.models import ContactForm, ContactMessages
from product.models import Category, Product
# Create your views here.


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    products_latest = Product.objects.all().order_by('-id')[:4]
    products_picked = Product.objects.all().order_by('?')[:4]
    page = "home"
    context = {
        'setting': setting,
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        'category': category
    }
    return render(request, 'index.html',context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {
        'setting': setting
    }
    return render(request, 'about.html',context)

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
            data.save()#save data to table 
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
    context = {
        'setting': setting,
        'page': page,
        'products': products,
        'category': category
    }
    return render(request, 'category_product.html', context)