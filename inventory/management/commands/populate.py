from django.core.management.base import BaseCommand
from inventory.models import User, Family, Category, Item, ItemTransaction, Checkin, Checkout
from datetime import date, timedelta

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
        today = date.today()
        five_days_ago = today - timedelta(days=5)
        ten_days_ago = today - timedelta(days=10)


        family = Family.objects.create(name="Jones-Indiana")
        family.save()
        print("Family has been created.")

        category1 = Category.objects.create(name="Clothes")
        category1.save()
        category2 = Category.objects.create(name="Expirable")
        category2.save()
        category3 = Category.objects.create(name="Expensive Items")
        category3.save()
        print("Category has been created.")

        item1 = Item.objects.create(category=category1, name="tshirt boys 4", price=10.56, quantity=10)
        item1.save()
        item2 = Item.objects.create(category=category1, name="jacket", price=13.50, quantity=18)
        item2.save()
        item3 = Item.objects.create(category=category3, name="stroller", price=45.00, quantity=5)
        item3.save()
        item4 = Item.objects.create(category=category2, name="formula", price=5.56, quantity=15)
        item4.save()
        print("Item has been created.")

        tx2 = ItemTransaction.objects.create(item=item3, quantity=1)
        tx2.save()
        tx3 = ItemTransaction.objects.create(item=item2, quantity=5)
        tx3.save()
        tx4 = ItemTransaction.objects.create(item=item4, quantity=3)
        tx4.save()
        tx1 = ItemTransaction.objects.create(item=item1, quantity=2)
        tx1.save()
        
        print("Transaction has been created.")

        staffUsr = User.objects.filter(first_name='Max').first()

        checkin = Checkin.objects.create(user=staffUsr, datetime=five_days_ago)
        checkin.items.add(tx1)
        checkin.save()

        checkin = Checkin.objects.create(user=staffUsr, datetime=ten_days_ago)
        checkin.items.add(tx2)
        checkin.save()
        print("Checkin has been created.")

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=five_days_ago)
        checkout.items.add(tx4)
        checkout.items.add(tx1)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=five_days_ago)
        checkout.items.add(tx2)
        checkout.items.add(tx1)
        checkout.items.add(tx4)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=five_days_ago)
        checkout.items.add(tx3)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=ten_days_ago)
        checkout.items.add(tx3)
        checkout.save()
        print("Checkout has been created.")
    
    def handle(self, *args, **options):
        self._create_users()
        self._create_sample_objects()
