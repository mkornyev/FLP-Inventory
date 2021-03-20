from django.core.management.base import BaseCommand
from inventory.models import User, Family, Category, Item, ItemTransaction, Checkin, Checkout

# DROP SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to destroy all objects.'

    def _destroy_users(self):
        User.objects.all().delete() 

        print("\nUsers deleted.\n")

    def _destroy_families(self):
        Family.objects.all().delete() 

        print("\nFamilies deleted.\n")

    def _destroy_categories(self):
        Category.objects.all().delete() 

        print("\nCategories deleted.\n")

    def _destroy_items(self):
        Item.objects.all().delete() 

        print("\nItems deleted.\n")

    def _destroy_item_transactions(self):
        ItemTransaction.objects.all().delete() 

        print("\nItemTransactions deleted.\n")

    def _destroy_checkins(self):
        Checkin.objects.all().delete() 

        print("\nCheckins deleted.\n")

    def _destroy_checkouts(self):
        Checkout.objects.all().delete() 

        print("\nCheckouts deleted.\n")

    def handle(self, *args, **options):
        self._destroy_checkins()
        self._destroy_checkouts()
        self._destroy_item_transactions()
        self._destroy_items()
        self._destroy_categories()
        self._destroy_families()
        self._destroy_users()
