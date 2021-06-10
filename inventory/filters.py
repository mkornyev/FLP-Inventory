import django_filters
from .models import Checkout, Item

class CheckoutFilter(django_filters.FilterSet):
    family__displayName = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Checkout
        fields = ['family__displayName']

class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['name']
