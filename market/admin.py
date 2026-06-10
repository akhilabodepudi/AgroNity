from django.contrib import admin
from .models import Crop, CartItem, Order

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('id','name','farmer','price','quantity','quality','health_status','created_at')
    search_fields = ('name','description','farmer__username')

admin.site.register(CartItem)
admin.site.register(Order)