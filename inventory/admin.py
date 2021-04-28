from django.contrib import admin

# Register your models here.

from .models import Family, Child, Category, Item, ItemTransaction, Checkin, Checkout, AgeRange

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname', 'phone', )
admin.site.register(Family, FamilyAdmin)

class ChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'family', )
admin.site.register(Child, ChildAdmin)

class AgeRangeAdmin(admin.ModelAdmin):
    list_display = ('low', 'high', )
admin.site.register(AgeRange, AgeRangeAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'quantity', 'new_price', 'used_price', )
admin.site.register(Item, ItemAdmin)

class ItemTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'is_new', )
admin.site.register(ItemTransaction, ItemTransactionAdmin)

class CheckinAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'in_items', 'datetime', )
admin.site.register(Checkin, CheckinAdmin)

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'family', 'childName', 'ageRange', 'out_items', 'datetime', 'notes', )
admin.site.register(Checkout, CheckoutAdmin)
