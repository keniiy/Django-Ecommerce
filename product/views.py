from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from product.models import CommentForm, Comment

# Create your views here.
def index(request):
    return HttpResponse("product")

def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    #return HttpResponse(url)
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = Comment()#create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip_address = request.META['REMOTE_ADDR']
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()#save data to table 
            messages.success(request, "Your Review has been sent. Thanks for Reviewing")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)