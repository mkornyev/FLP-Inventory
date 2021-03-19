from django.contrib import admin

# Register your models here.
from .models import Family, Category, Item, ItemTransaction, Checkin, Checkout

admin.site.register(Family)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemTransaction)
admin.site.register(Checkin)
admin.site.register(Checkout)
