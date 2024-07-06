from django.contrib import admin

from .models import ShppingAddress, Order, OrderItem

# Register your models here.


admin.site.register(ShppingAddress)

admin.site.register(Order)

admin.site.register(OrderItem)