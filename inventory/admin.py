# from django.contrib import admin

# Register your models here.

from .models import Family, Category, Item, ItemTransaction, Checkin, Checkout

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', )
admin.site.register(Family, FamilyAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price', )
admin.site.register(Item, ItemAdmin)

class ItemTransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', )
admin.site.register(ItemTransaction, ItemTransactionAdmin)

class CheckinAdmin(admin.ModelAdmin):
    list_display = ('user', 'in_items', 'datetime', )
admin.site.register(Checkin, CheckinAdmin)

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'family', 'out_items', 'datetime', )
admin.site.register(Checkout, CheckoutAdmin)
