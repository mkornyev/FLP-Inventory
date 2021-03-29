from django.core.management.base import BaseCommand
from inventory.models import Family, Category, Item, ItemTransaction, Checkin, Checkout
import csv


class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to email CSV backup of db.'

    def write_model_to_csv(self, model):
        qs = model.objects
        filename = f'./db_csv_backups/{model.__name__}.csv'
        outfile = open(filename,'w')
        field_names = [f.name for f in model._meta.local_fields]
        writer = csv.writer(outfile)
        writer.writerow(field_names)
        for i in qs.all():
            row = [str(getattr(i, f)) for f in field_names]
            writer.writerow(row)

    def handle(self, *args, **options):
        for model in [Family, Category, Item, ItemTransaction, Checkin, Checkout]:
            self.write_model_to_csv(model)
        