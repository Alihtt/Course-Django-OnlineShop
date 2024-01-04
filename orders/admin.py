from django.contrib import admin
from .models import OrderItem, Order, Coupon

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


admin.site.register(Coupon)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid', 'created')
    list_filter = ('paid',)
    inlines = (OrderItemInline,)
