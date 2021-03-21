from django.core.management.base import BaseCommand
from inventory.models import User, Family, Category, Item, ItemTransaction, Checkin, Checkout

# POPULATE SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to create sample model objects.'

    def _create_users(self):
        admin = User.objects.create_user(username='admin', password='admin', first_name='Kelly', last_name='Hughes', email='flpadmin@gmail.com')
        admin.is_staff = True 
        admin.is_superuser = True
        admin.save()
        
        print("\nAdmin has been created.")

        sow = User.objects.create_user(username='staff', password='staff', first_name='Max', last_name='K', email='mk@gmail.com')
        sow.is_staff = True 
        sow.is_superuser = False
        sow.save()

        print("Staff has been created.")

    def _create_sample_objects(self):

        family = Family.objects.create(name="Jones-Indiana")
        family.save()
        print("Family has been created.")

        category = Category.objects.create(name="Clothes")
        category.save()
        print("Category has been created.")

        shirt = Item.objects.create(category=category, name="tshirt boys 4", price=10.56, quantity=10)
        shirt.save()
        print("Item has been created.")

        transaction = ItemTransaction.objects.create(item=shirt, quantity=2)
        transaction.save()
        print("Transaction has been created.")

        staffUsr = User.objects.filter(first_name='Max').first()

        checkin = Checkin.objects.create(user=staffUsr)
        checkin.items.add(transaction)
        checkin.save()
        print("Checkin has been created.")

        checkout = Checkout.objects.create(user=staffUsr, family=family)
        checkout.items.add(transaction)
        checkout.save()
        print("Checkout has been created.")
    
    def handle(self, *args, **options):
        self._create_users()
        self._create_sample_objects()
