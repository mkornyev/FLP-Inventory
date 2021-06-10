import django_filters
from .models import Checkout, Item

class CheckoutFilter(django_filters.FilterSet):
    family__displayName = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Checkout
        fields = ['family__displayName']

class ItemFilter(django_filters.FilterSet):
    item__name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Item
        fields = ['item__name']
