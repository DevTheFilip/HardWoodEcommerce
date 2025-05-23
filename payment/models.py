from django.db import models


from django.contrib.auth.models import User


from store.models import Product

#oder model

class Order(models.Model):
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.CharField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_odered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100, default="Pending")

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return 'Order - #' +str(self.id)


class OrderItem(models.Model):
    #FK->
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return 'Order Item - #' +str(self.id)


# Create your models here.

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20)


    #KF
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)



    class Meta:
       verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return 'Shipping Adress - ' +str(self.id)
