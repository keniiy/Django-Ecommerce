from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, Textarea, TextInput, Select
# Create your models here.

class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    company = models.CharField(max_length=300)
    address = models.CharField(blank=True,max_length=300)
    phone = models.CharField(blank=True,max_length=14)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=300)
    smtpserver = models.CharField(blank=True,max_length=20)
    smtppasword = models.CharField(blank=True,max_length=100)
    smtpemail = models.CharField(blank=True,max_length=20)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True,max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    stared = RichTextUploadingField(blank=True)
    vision = RichTextUploadingField(blank=True)
    mission = RichTextUploadingField(blank=True)
    goal = RichTextUploadingField(blank=True)
    importance = RichTextUploadingField(blank=True)
    fast_delivery = RichTextUploadingField(blank=True)
    secure_payment = RichTextUploadingField(blank=True)
    support = RichTextUploadingField(blank=True)
    quality_product = RichTextUploadingField(blank=True)
    money_back_guarntee = RichTextUploadingField(blank=True)
    free_return = RichTextUploadingField(blank=True)
    about_ceo = RichTextUploadingField(blank=True)
    ceo_image = models.ImageField(blank=True, upload_to='images/')
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=300,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactMessages(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
    telephone = models.CharField(max_length=14)
    status = models.CharField(choices=STATUS,max_length=6,default='New')
    ip_address = models.CharField(blank=True,max_length=20)
    note = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessages
        fields = ['name', 'email', 'subject','telephone','message']
        widgets = {
            'name'   : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
            'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
            'email'   : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
            'telephone'   : TextInput(attrs={'class': 'input','placeholder':'Phone No'}),
            'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message', 'row':'7 '}),
        }

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question