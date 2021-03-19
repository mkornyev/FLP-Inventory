from django.core.management.base import BaseCommand
from inventory.models import User, Family, Category, Item, ItemTransaction, Checkin, Checkout

# DROP SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to destroy all objects.'

    def _destroy_users(self):
        users = User.objects.all()

        for u in users:
            u.delete() 

        print("\nUsers deleted.\n")

    def _destroy_families(self):
        families = Family.objects.all()

        for x in families:
            x.delete() 

        print("\nFamilies deleted.\n")

    def _destroy_categories(self):
        categories = Category.objects.all()

        for x in categories:
            x.delete() 

        print("\nCategories deleted.\n")

    def _destroy_items(self):
        items = Item.objects.all()

        for x in items:
            x.delete() 

        print("\nItems deleted.\n")

    def _destroy_item_transactions(self):
        item_transactions = ItemTransaction.objects.all()

        for x in item_transactions:
            x.delete() 

        print("\nItemTransactions deleted.\n")

    def _destroy_checkins(self):
        checkins = Checkin.objects.all()

        for x in checkins:
            x.delete() 

        print("\nCheckins deleted.\n")

    def _destroy_checkouts(self):
        checkouts = Checkout.objects.all()

        for x in checkouts:
            x.delete() 

        print("\nCheckouts deleted.\n")

    def handle(self, *args, **options):
        self._destroy_checkins()
        self._destroy_checkouts()
        self._destroy_item_transactions()
        self._destroy_items()
        self._destroy_categories()
        self._destroy_families()
        self._destroy_users()
