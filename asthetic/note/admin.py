from django.contrib import admin
from .models import Note ,Room,Departments,Semester,Customer,Order,OrderItem,ShippingAddress

# Register your models here.
admin.site.register(Note)
admin.site.register(Room)
admin.site.register(Departments)
admin.site.register(Semester)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)





