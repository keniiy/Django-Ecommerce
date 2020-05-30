from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.forms import ModelForm

# Create your models here.
class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return(self.product.price)

    @property
    def amount(self):
        return(self.quantity * self.product.price)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']