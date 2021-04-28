from django.core.management.base import BaseCommand
from inventory.models import User, Family, Child, Category, Item, ItemTransaction, Checkin, Checkout, AgeRange
from datetime import date, timedelta
import os

# POPULATE SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to create sample model objects.'

    def _create_users(self):
        admin = User.objects.create_user(username='admin', password=os.environ['ADMIN_USER_PASS'], first_name='Kelly', last_name='Hughes', email='flpadmin@gmail.com')
        admin.is_staff = True 
        admin.is_superuser = True
        admin.save()
        
        print("\nAdmin has been created.")

        sow = User.objects.create_user(username='staff', password=os.environ['STAFF_USER_PASS'], first_name='Max', last_name='K', email='mk@gmail.com')
        sow.is_staff = True 
        sow.is_superuser = False
        sow.save()

        print("Staff has been created.")

    def _create_sample_objects(self):
        today = date.today()
        five_days_ago = today - timedelta(days=5)
        ten_days_ago = today - timedelta(days=10)

        family = Family.objects.create(lname="Jones-Indiana")
        family.save()
        family = Family.objects.create(lname="Pavetti", phone="+1234567891")
        family.save()
        family = Family.objects.create(fname="Paulo", lname="Merson", phone="1234567891")
        family.save()
        print("Family has been created.")

        child = Child.objects.create(name="Paulo Jr", family=family)
        child.save()
        print("Children have been created.")

        category1 = Category.objects.create(name="Clothes")
        category1.save()
        category2 = Category.objects.create(name="Expirable")
        category2.save()
        category3 = Category.objects.create(name="Expensive Items")
        category3.save()
        print("Category has been created.")


        a0to1 = AgeRange.objects.create(low=0, high=1)
        a1to2 = AgeRange.objects.create(low=1, high=2)
        a3to5 = AgeRange.objects.create(low=3, high=5)
        a6to8 = AgeRange.objects.create(low=6, high=8)
        a9to12 = AgeRange.objects.create(low=9, high=12)
        a13to15 = AgeRange.objects.create(low=13, high=15)
        a0to1.save()
        a1to2.save()
        a3to5.save()
        a6to8.save()
        a9to12.save()
        a13to15.save()
        print("Age ranges created")

        item1 = Item.objects.create(category=category1, name="tshirt boys 4", new_price=10.56, used_price=7.20, quantity=10)
        item1.save()
        item2 = Item.objects.create(category=category1, name="jacket", quantity=18) # No Price 
        item2.save()
        item3 = Item.objects.create(category=category3, name="stroller", new_price=45.00, quantity=5)
        item3.save()
        item4 = Item.objects.create(category=category2, name="formula", used_price=5.50, quantity=15)
        item4.save()
        item5 = Item.objects.create(category=category1, name="t shirt girls 4", new_price=2.00, used_price=1.00, quantity=3)
        item5.save()
        print("Item has been created.")

        tx2 = ItemTransaction.objects.create(item=item3, quantity=1)
        tx2.save()
        tx3 = ItemTransaction.objects.create(item=item2, quantity=5, is_new=True)
        tx3.save()
        tx4 = ItemTransaction.objects.create(item=item4, quantity=3)
        tx4.save()
        tx1 = ItemTransaction.objects.create(item=item1, quantity=2)
        tx1.save()
        tx5 = ItemTransaction.objects.create(item=item5, quantity=3, is_new=True)
        tx5.save()
        tx6 = ItemTransaction.objects.create(item=item5, quantity=1)
        tx6.save()
        
        print("Transaction has been created.")

        staffUsr = User.objects.filter(first_name='Max').first()

        checkin = Checkin.objects.create(user=staffUsr, datetime=five_days_ago)
        checkin.items.add(tx1)
        checkin.save()

        checkin = Checkin.objects.create(user=staffUsr, datetime=ten_days_ago)
        checkin.items.add(tx2)
        checkin.save()

        checkin = Checkin.objects.create(user=staffUsr, datetime=today)
        checkin.items.add(tx5)
        checkin.save()
        print("Checkin has been created.")

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=five_days_ago, ageRange=a9to12)
        checkout.items.add(tx4)
        checkout.items.add(tx1)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=five_days_ago, ageRange=a0to1, notes="The stroller is brand new, retails for ~$80")
        checkout.items.add(tx2)
        checkout.items.add(tx1)
        checkout.items.add(tx4)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=five_days_ago, ageRange=a0to1, childName="Sunny")
        checkout.items.add(tx3)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=ten_days_ago, ageRange=a6to8, childName="Sean")
        checkout.items.add(tx3)
        checkout.save()
        
        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=today, ageRange=a3to5, childName="Luke")
        checkout.items.add(tx5)
        checkout.save()

        checkout = Checkout.objects.create(user=staffUsr, family=family, datetime=today, ageRange=a1to2, notes="Not sure what these shirts cost??? - Krissy")
        checkout.items.add(tx6)
        checkout.save()
        print("Checkout has been created.")
    
    def handle(self, *args, **options):
        self._create_users()
        self._create_sample_objects()
