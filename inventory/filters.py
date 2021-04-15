import django_filters
from .models import Checkout

class CheckoutFilter(django_filters.FilterSet):
    family__name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Checkout
        fields = ['family__name']
