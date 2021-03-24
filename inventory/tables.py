import django_tables2 as tables
from .models import Family, Category, Item, Checkin, Checkout

from django.db.models import F
from django.db.models import Func

# Provide ordering methods for model with a name field
class NameTable(tables.Table):
    # order by names alphabetically, case-insensitive
     def order_name(self, queryset, is_descending):
        queryset = queryset.annotate(
            lower=Func(F('name'), function='LOWER')
        ).order_by(("-" if is_descending else "") + "lower")
        return (queryset, True)

class FamilyTable(NameTable):
    class Meta:
        model = Family
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", )
        order_by = 'name'

class CategoryTable(NameTable):
    class Meta:
        model = Category
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", )
        order_by = 'name'

class ItemTable(NameTable):  
    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "category", "price", "quantity", )
        order_by = 'name'

class CheckinTable(tables.Table):   
    class Meta:
        model = Checkin
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "user", "datetime", "in_items", )
        order_by = 'datetime'

class CheckoutTable(tables.Table):
    class Meta:
        model = Checkout
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "user", "family.name", "datetime", "out_items", )
        order_by = 'datetime'