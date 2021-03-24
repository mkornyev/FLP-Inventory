import django_tables2 as tables
from .models import Item

from django.db.models import F
from django.db.models import Func

class ItemTable(tables.Table):
    
    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "category", "price", "quantity", )
        order_by = 'name'
    
    def order_name(self, queryset, is_descending):
        queryset = queryset.annotate(
            lower=Func(F('name'), function='LOWER')
        ).order_by(("-" if is_descending else "") + "lower")
        return (queryset, True)
