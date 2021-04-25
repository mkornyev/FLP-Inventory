from django.core.management.base import BaseCommand
from inventory.models import User, Family, Child, Category, Item, ItemTransaction, Checkin, Checkout, AgeRange

# DROP SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to destroy all objects.'

    def _destroy_users(self):
        User.objects.all().delete() 

        print("Users deleted.")

    def _destroy_families(self):
        Family.objects.all().delete() 

        print("Families deleted.")

    def _destroy_children(self):
        Child.objects.all().delete() 

        print("Children deleted.")

    def _destroy_children(self):
        AgeRange.objects.all().delete() 

        print("AgeRange deleted.")

    def _destroy_categories(self):
        Category.objects.all().delete() 

        print("Categories deleted.")

    def _destroy_items(self):
        Item.objects.all().delete() 

        print("Items deleted.")

    def _destroy_item_transactions(self):
        ItemTransaction.objects.all().delete() 

        print("ItemTransactions deleted.")

    def _destroy_checkins(self):
        Checkin.objects.all().delete() 

        print("\nCheckins deleted.")

    def _destroy_checkouts(self):
        Checkout.objects.all().delete() 

        print("Checkouts deleted.")

    def handle(self, *args, **options):
        self._destroy_checkins()
        self._destroy_checkouts()
        self._destroy_item_transactions()
        self._destroy_items()
        self._destroy_categories()
        self._destroy_children()
        self._destroy_families()
        self._destroy_users()
