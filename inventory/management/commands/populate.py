from django.core.management.base import BaseCommand
from inventory.models import User, Family, Category, Item, ItemTransaction, Checkin, Checkout

# POPULATE SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to create sample model objects.'

    def _create_users(self):
        admin = User.objects.create_user(username='admintaili', password='gy!e12uNAs', first_name='Taili', last_name='Thompson', email='bvbaseball42@gmail.com')
        admin.is_staff = True 
        admin.is_superuser = True
        admin.save()
        
        print("\nAdmin has been created.\n")

    def _create_sample_objects(self):
      sow = User.objects.create_user(username='sow', password='sow', first_name='Max', last_name='K', email='mkornyev@gmail.com')
      sow.is_staff = True 
      sow.is_superuser = False
      sow.save()

      print("Staff has been created.\n")

      family = Family.objects.create(name="Jones-Indiana")
      family.save()
      print("Family has been created.\n")

      category = Category.objects.create(name="Clothes")
      category.save()
      print("Category has been created.\n")

      shirt = Item.objects.create(category=category, name="tshirt boys 4", price=10.56, quantity=10)
      shirt.save()
      print("Item has been created.\n")

      transaction = ItemTransaction.objects.create(item=shirt, quantity=2)
      transaction.save()
      print("Transaction has been created.\n")

      checkin = Checkin.objects.create(user=sow)
      checkin.items.add(transaction)
      checkin.save()
      print("Checkin has been created.\n")

      checkout = Checkout.objects.create(user=sow, family=family)
      checkout.items.add(transaction)
      checkout.save()
      print("Checkout has been created.\n")
    
    def handle(self, *args, **options):
      self._create_users()
      self._create_sample_objects()
