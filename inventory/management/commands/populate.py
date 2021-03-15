from django.core.management.base import BaseCommand
# from inventory.models import User

# POPULATE SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to create sample model objects.'

    # some sample code i stole from another project:
    
    # def _create_users(self):
    #     """
    #     sow = User.objects.create_user(username='sow', password='sow', first_name='Max', last_name='K', email='mkornyev@gmail.com')
    #     sow.is_staff = True 
    #     sow.is_superuser = False
    #     sow.save()
    #     """
    #     admin = User.objects.create_user(username='admintaili', password='gy!e12uNAs', first_name='Taili', last_name='Thompson', email='bvbaseball42@gmail.com')
    #     admin.is_staff = True 
    #     admin.is_superuser = True
    #     admin.save()
        
    #     print("\nAdmin has been created.\n")

    def handle(self, *args, **options):
      pass
        # self._create_users()
