#!/usr/bin/python
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import openpyxl

class Command(BaseCommand):
    args = 'this function takes three arguments, the paths to the \
            Sharepoint manage inventory excel file, Sharepoint manage items excel file, \
            and initial master list of items excel file'
    help = 'Download the "Manage Inventory" and "Manage Items"  pages\' from Sharepoint \
            and the master list of items used to initialize Sharepoint and provide \
            the path to these files as arguments'
    
    def add_arguments(self, parser):
        parser.add_argument('manage_inventory')
        parser.add_argument('manage_items')
        parser.add_argument('masterlist')

    def handle(self, *args, **options):
        INVENTORY_FILE_PATH = options['manage_inventory']
        ITEMS_FILE_PATH = options['manage_items']
        MASTERLIST_PATH = options['masterlist']

        items = dict()

        inventory_sheet = openpyxl.load_workbook(MASTERLIST_PATH).active
        items_sheet = openpyxl.load_workbook(ITEMS_FILE_PATH).active
        masterlist_sheet = openpyxl.load_workbook(MASTERLIST_PATH).active

        for r in inventory_sheet.iter_rows(min_row=2): # skip header
            item_name = r[2].value
            count = r[5].value
            quantities[item_name] = count
        for r in items_sheet.iter_rows(min_rows=2):
            item_name = r[2].value
            category = r[3].value
            categories[item_name] = 

        
            # item1 = Item.objects.create(category=category1, name="tshirt boys 4", price=10.56, quantity=10)
            # item1.save()
