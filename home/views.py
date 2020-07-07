from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from home.models import ContactForm, ContactMessages, Setting
from product.models import Category, Product, Images, Comment, Variants
from home.forms import SearchForm
from django.db.models import Q
import json



def index(request):
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
    setting = Setting.objects.get(pk=1)
    context = {
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
        'category': category,
        'setting': setting,
        
    }
    return render(request, 'index.html', context)

def aboutus(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'setting': setting,
        'category': category,
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
    category = Category.objects.all()
    form = ContactForm
    context = {
        'setting': setting,
        'category': category,
        'form': form
    }
    return render(request, 'contact.html',context)

def category_products(request,id,slug):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    top_rated = Product.objects.all().order_by('-id')[:6]
    catdata = Category.objects.get(pk=id)
    context = {
        'products': products,
        'category': category,
        'catdata': catdata,
        'setting': setting,
        'top_rated': top_rated
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

    setting = Setting.objects.get(pk=1)
    top_rated = Product.objects.all().order_by('-id')[:6]
    category = Category.objects.all()
    context = {
        'top_rated': top_rated,
        'setting': setting,
        'querysets': querysets,
        'category': category
    }
    return render(request, 'search_products.html', context)

def product_detail(request,id,slug):
    related_product = Product.objects.all().order_by('?')[:6]
    setting = Setting.objects.get(pk=1)
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'product': product,
               'category': category,
               'images': images,
               'comments': comments,
               'related_product': related_product,
               'setting': setting
               }
    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes,
                        'colors': colors,
                        'variant': variant,
                        'query': query,
                        })
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)