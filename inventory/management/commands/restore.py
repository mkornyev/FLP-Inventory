from django.core.management.base import BaseCommand
from inventory.models import *
from django.utils.dateparse import parse_datetime
import csv, os
import sqlite3


class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Create a folder in root directory named db_csv_backups(this folder will not be uploaded to remote by .gitignore),\
        run this command and all database will be restored with six database backup csvs in the folder.\
        WILL NOT make any change to non-empty tables.\
        Combine with populate -c to restore preset age ranges'
    
    def _restore_users(self):
        if len(User.objects.all()) != 0:
            return
        admin = User.objects.create_user(username='angie', password=os.environ['ADMIN_USER_PASS'], first_name='Angela', last_name='Damiano', email='hello@fosterloveproject.org')
        admin.is_staff = True 
        admin.is_superuser = True
        admin.save()
        print("NO USERS FOUND, CREATING DUMIES.")
        
    def _restore_Category(self):
        if len(Category.objects.all()) != 0:
            return
        dataReader = csv.reader(open("db_csv_backups/Category.csv"), delimiter=',', quotechar='"')
        count = 0
        for row in dataReader:
            count = count + 1
            if count == 1:
                continue
            Category.objects.create(id = row[0], name=row[1])
        print("%d Category records has been restored." % count)
            
    def _restore_Family(self):
        if len(Family.objects.all()) != 0:
            return
        dataReader = csv.reader(open("db_csv_backups/Family.csv"), delimiter=',', quotechar='"')
        count = 0
        for row in dataReader:
            count = count + 1
            if count == 1:
                continue
            Family.objects.create(id = row[0], fname = row[1], lname = row[2], phone = row[3], displayName = row[4])
        print("%d Family records has been restored." % count)

    def _restore_Item(self):
        if len(Item.objects.all()) != 0:
            return
        dataReader = csv.reader(open("db_csv_backups/Item.csv"), delimiter=',', quotechar='"')
        count = 0
        for row in dataReader:
            count = count + 1
            if count == 1:
                continue
            r3 = r4 = None
            if row[3] != "":
                r3 = float(row[3])
            if row[4] != "":
                r4 = float(row[4])
            if Category.objects.filter(name = row[1]).exists():
                Item.objects.create(id = row[0], category = Category.objects.get(name = row[1]), name = row[2], new_price = r3, used_price = r4, quantity = int(row[5]))
            else:
                Item.objects.create(id = row[0], name = row[2], new_price = r3, used_price = r4, quantity = int(row[5]))
            
            
        print("%d Item records has been restored." % count)
    
    def _restore_ItemTransaction(self):
        if len(ItemTransaction.objects.all()) != 0:
            return
        dataReader = csv.reader(open("db_csv_backups/ItemTransaction.csv"), delimiter=',', quotechar='"')
        count = 0
        for row in dataReader:
            count = count + 1
            if count == 1:
                continue
            if Item.objects.filter(name = row[1]).exists():
                itm = None
            else:
                itm = Item.objects.get(name = row[1])
            ItemTransaction.objects.create(id = row[0], item = itm, quantity = int(row[2]), is_new = row[3])
        print("%d ItemTransaction records has been restored." % count)
        
    def _restore_Checkin(self):
        if len(Checkin.objects.all()) != 0:
            return
        dataReader = csv.reader(open("db_csv_backups/Checkin.csv"), delimiter=',', quotechar='"')
        count = 0
        for row in dataReader:
            count = count + 1
            if count == 1:
                continue
            if User.objects.filter(username = row[1]).exists():
                usr = None
            else:
                usr = User.objects.get(username = row[1])
            r4 = None
            if row[4] != "":
                r4 = row[4]
            Checkin.objects.create(id = row[0], user = usr, datetime = parse_datetime(row[2]), items = row[3], notes = r4)
        print("%d Checkin records has been restored." % count)
    
    def _restore_Checkout(self):
        if len(Checkout.objects.all()) != 0:
            return
        dataReader = csv.reader(open("db_csv_backups/Checkout.csv"), delimiter=',', quotechar='"')
        count = 0
        for row in dataReader:
            count = count + 1
            if count == 1:
                continue
            Checkout.objects.create(id = row[0], user = User.objects.get(username = row[1]), datetime = parse_datetime(row[2]), items = row[3], notes = row[4])
        print("%d Checkout records has been restored." % count)
    
    def _overwrite(self):
        conn_backup = None
        conn = None
        try:
            conn_backup = sqlite3.connect("db_backups/db0.sqlite3")
            cur_backup = conn_backup.cursor()
        except sqlite3.Error as e:
            print(e)
        try:
            conn = sqlite3.connect("db.sqlite3")
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
        
        cur_backup.execute("SELECT * FROM inventory_itemtransaction")
        rows = cur_backup.fetchall()

        cur.executemany("INSERT INTO inventory_itemtransaction VALUES(?,?,?,?);", rows)
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory_itemtransaction")
        rows = cur.fetchall()
        for r in rows:
            print(r)

    # def _reset(self):
        
    def handle(self, *args, **options):
        # self._reset()
        self._overwrite()
        # self._restore_users()
        # self._restore_Category()
        # self._restore_Family()
        # self._restore_Item()
        # self._restore_ItemTransaction()
        # self._restore_Checkin()
        # self._restore_Checkout()
        
        