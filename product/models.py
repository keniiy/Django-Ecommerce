from django.db import models

# Create your models here.

class Category(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent=models.ForeignKey('self',blank=True, null=True , related_name='children',on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('True', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='1')
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = models.TextField(blank=True)
    slug = models.SlugField()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    #methos to create a fake database table field in read only mode
    def image_tag(self):
        return marksafe('<img src"{}" height="50"/>'.format(self.image.url))

    image_tag.shortdescription = 'Image'
