from django.contrib import admin
from .models import Orders

# Register your models here.

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'status', 'offer_type', 'customer', 'seller']

    def customer(self, obj):
        return obj.customer_user.username
    customer.short_description = 'Customer'

    def seller(self, obj):
        return obj.business_user.username
    seller.short_description = 'Seller'