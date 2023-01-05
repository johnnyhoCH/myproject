from django.db import models

# Create your models here.


class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    custom_name = models.CharField(max_length=100)
    custom_email = models.CharField(max_length=100)
    custom_phone = models.CharField(max_length=30)
    pay_type = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    custom_address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.custom_name
    
class DetailModel(models.Model):
    dorder = models.ForeignKey("OrdersModel",on_delete=models.CASCADE)
    product_name = models.CharField(max_length=80)
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.pname