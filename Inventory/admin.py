from django.contrib import admin
from .models import Category , Supplier , InventoryItem , InventoryRecord ,  OrderItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(InventoryItem)
admin.site.register(InventoryRecord)
admin.site.register(OrderItem)
