from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from inventory.models import Family, Category, Item, ItemTransaction, Checkin, Checkout
import csv, os
from datetime import datetime

MODELS_TO_BACKUP = [Family, Category, Item, ItemTransaction, Checkin, Checkout]

class Command(BaseCommand):
    args = 'this function takes one argument, which is the email you want to send the backups to'
    help = 'Try `python3 manage.py csv EMAIL_ADDRESS`'

    def add_arguments(self, parser):
        parser.add_argument('email')

    def write_model_to_csv(self, model):
        qs = model.objects.all()
        filename = f'./db_csv_backups/{model.__name__}.csv'
        outfile = open(filename,'w')
        field_names = [f.name for f in qs.model._meta.get_fields()]
        writer = csv.writer(outfile)
        heading = []
        if len(qs) != 0:
            for f in field_names:
                if hasattr(qs[0], f):
                    heading.append(f)
        rows = []
        for i in qs:
            row = []
            for f in field_names:
                if hasattr(i, f):
                    if f == "items":
                        txs = ', '.join([str(tx) for tx in i.items.all()])
                        row.append(txs)
                    else:
                        row.append(getattr(i, f))
            rows.append(row)
        writer.writerow(heading)
        writer.writerows(rows)

    def send_email(self, to_email_addr):
        date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        email = EmailMessage(
            f'Database backup CSV\'s: {date}',
            f'Please find attached CSV backups of the FLP inventory system as of {date}',
            'flpinventory@gmail.com',
            [to_email_addr],
            [],
            reply_to=['flpinventory@gmail.com'],
            headers={},
        )
        path = './db_csv_backups/'
        for fname in os.listdir(path):
            email.attach(fname, open(path+fname, 'r').read())
        email.send()


    def handle(self, *args, **options):
        addr = options['email']
        for model in MODELS_TO_BACKUP:
            self.write_model_to_csv(model)
        self.send_email(addr)
