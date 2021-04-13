import django_filters
from .models import Checkout

class CheckoutFilter(django_filters.FilterSet):
    class Meta:
        model = Checkout
        fields = ['family__name']
