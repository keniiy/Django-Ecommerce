from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

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
    email =  models.CharField(blank=True,max_length=300)
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
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=300,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title