from django.db import models
from store.models import Product, Variation
from django.contrib.auth.models import User
from accounts.models import Accounts


# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, blank=True, null=True)
    variation = models.ManyToManyField(Variation, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    Quantity =  models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.Quantity
    
  
    def __unicode__(self):
        return self.product
