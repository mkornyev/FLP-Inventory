from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from inventory.models import Family, Category, Item, ItemTransaction, Checkin, Checkout
import csv, os
from datetime import datetime
from zipfile import ZipFile
from email.mime.application import MIMEApplication

MODELS_TO_BACKUP = [Family, Category, Item, ItemTransaction, Checkin, Checkout]
ZIPFILE_NAME = 'backup.zip'
PATH = './db_csv_backups/'

class Command(BaseCommand):
    args = 'this function takes one argument, which is the email you want to send the backups to'
    help = 'Try `python3 manage.py csv EMAIL_ADDRESS`'

    def add_arguments(self, parser):
        parser.add_argument('email')

    def write_model_to_csv(self, model):
        qs = model.objects.all()
        if not os.path.exists('db_csv_backups'):
            os.makedirs('db_csv_backups')
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

    def zip_files(self):
        with ZipFile(PATH+ZIPFILE_NAME,'w') as zip:
            for fname in os.listdir(PATH):
                if "csv" in fname:
                    zip.write(PATH+fname)

    def send_email(self, to_email_addr):
        date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        email = EmailMessage(
            f'Database backup CSV\'s: {date}',
            f'Please find attached zipped CSV backups of the FLP inventory system as of {date}. ',
            'flpinventory@gmail.com',
            [to_email_addr],
            [],
            reply_to=['flpinventory@gmail.com'],
            headers={},
        )
        with open(PATH+ZIPFILE_NAME,'rb') as file:
            email.attach(MIMEApplication(file.read(), Name=ZIPFILE_NAME))
        email.send()


    def handle(self, *args, **options):
        addr = options['email']
        for model in MODELS_TO_BACKUP:
            self.write_model_to_csv(model)
        self.zip_files()
        self.send_email(addr)
