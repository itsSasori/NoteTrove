from typing import Any
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name



class Note(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


    

class Departments(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Semester(models.Model):
    department = models.ForeignKey(Departments , on_delete=models.CASCADE)
    name=models.CharField(max_length=100)


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    department=models.ForeignKey(Departments,on_delete=models.CASCADE)
    semester= models.ForeignKey(Semester, on_delete=models.CASCADE)
    image = models.ImageField(null=True, default="avatar.svg")
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
    @property

    def ImageURL(self):
          
          try:
                
                url = self.image.url
          except:
                url=''
          return url
                


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    

    def __str__(self):
        return str(self.id) # type: ignore


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() # type: ignore
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() # type: ignore
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
              
    @property
    def get_total(self):
        if self.quantity is not None and self.product is not None and self.product.price is not None:
            return self.product.price * self.quantity
        return 0
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all() # type: ignore
        for i in orderitems:
            if i.product.digital == False:
                shipping =True
        return shipping

        

class ShippingAddress(models.Model):
        
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address






