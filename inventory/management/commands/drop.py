from django.core.management.base import BaseCommand
# from inventory.models import User

# DROP SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to create sample users.'

    # some sample code I stole from an old project: 
    
    # def _destroy_users(self):
    #     users = User.objects.all()

    #     for u in users:
    #         u.delete() 

    #     print("\nUsers deleted.\n")

    def handle(self, *args, **options):
      pass
      # self._destroy_users()