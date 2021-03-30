from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from inventory.models import Family, Category, Item, ItemTransaction, Checkin, Checkout
import csv, os

MODELS_TO_BACKUP = [Family, Category, Item, ItemTransaction, Checkin, Checkout]

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

    def send_email(self):
        email = EmailMessage(
            'Database backup CSV\'s',
            'Please find attached CSV backups of the FLP inventory system.',
            'flpinventory@gmail.com',
            [settings.TO_EMAIL],
            [],
            reply_to=['flpinventory@gmail.com'],
            headers={},
        )
        path = './db_csv_backups/'
        for fname in os.listdir(path):
            email.attach(fname, open(path+fname, 'r').read())
        email.send()


    def handle(self, *args, **options):
        for model in MODELS_TO_BACKUP:
            self.write_model_to_csv(model)
        self.send_email()
