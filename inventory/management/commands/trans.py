from django.core.management.base import BaseCommand
from inventory.models import Item, ItemTransaction

# MIGRATION SCRIPT

class Command(BaseCommand):
    args = '<this func takes no args>'
    help = 'Run this script to migrate old database into newly designed one.'

    #NEW_ITEM_NAMES = ["shirt", "shoes", "underwear", "socks", "pj", "shorts", "pants", "sweater/sweartshirt", "coat/jacket", "dress/skirt", "accessories", "other", "snowsuit", "onesie"]
    NEW_ITEM_NAMES = []
    NEW_SIZES = ["baby", "toddler", "kid", "teen"]

    def itemMap(itemName):
        item_mapped = "" 
        size_mapped = ""
        if ("boy" in itemName) or ("girl" in itemName):
            if itemName.startswith("boys "):
                name_new = itemName[len("boys "):]
                item_mapped = name_new.split()[0]
            elif itemName.startswith("girls "):
                name_new = itemName[len("girls "):]
                item_mapped = name_new.split()[0]
            elif itemName.endswith("boy)"): 
                name_new = itemName
                item_mapped = name_new.split()[0]
            elif itemName.endswith("girl)"):
                name_new = itemName
                item_mapped = name_new.split()[0]
            else:
                raise Exception("ill-formatted string detected: "+itemName)
                
            if (len(name_new.split()) > 1) and name_new.split()[1] == "socks":
                item_mapped = "socks"
            if ("snowsuit" in item_mapped):  #this branch is to cope with one typo, no subtle way to put this.
                item_mapped = "snowsuit"
            if ("coat" in item_mapped) or ("jacket" in item_mapped):
                    item_mapped = "coat/jacket"
            if "pj" in item_mapped:
                    item_mapped = "pj"

            if ("teen" in name_new) or ("14-16" in name_new) or ("18-20" in name_new):
                size_mapped = "teen"
            elif ("kid" in name_new) or ("6-7" in name_new) or ("8-10" in name_new) or ("10-12" in name_new) or ("12-14" in name_new):
                size_mapped = "kid"
            elif ("infant" in name_new) or (" mo" in name_new) or ("baby" in name_new):
                size_mapped = "baby"
            elif ("T" in name_new) or ("toddler" in name_new):
                size_mapped = "toddler"
            else:
                size_mapped = "kid"
        else:
            raise Exception("ill-formatted input string")
        return item_mapped, size_mapped


    def _add_outdated(self):
        for t in Item.objects.all():
            if ("boy" in t.name) or ("girl" in t.name):
                t.outdated = True
                t.save()
        print("Items updated.\n")

    def _add_newitems(self):
        for t in Item.objects.all():
            name = t.name
            if ("boys" in name) or ("girls" in name):
                item_mapped, size_mapped = Command.itemMap(name)
                if not(item_mapped in Command.NEW_ITEM_NAMES):
                    Command.NEW_ITEM_NAMES.append(item_mapped)
        print("all new items to be created:",  Command.NEW_ITEM_NAMES, "\n")
        for item in Command.NEW_ITEM_NAMES:
            for size in Command.NEW_SIZES:
                # print("creating item: "+ item+" "+size +" \n")
                if (item == "bra") and (size == "baby" or size == "toddler"):
                    continue
                Item.objects.create(name=item + " " + size, quantity=0)
                # TODO: add default category Category.objects.get(name__exact="Clothing")
                print("created item: "+ item + " "+size +" \n")
                    
    def _update_newitems(self):
        for t in Item.objects.all():
            name = t.name
            if ("boys" in name) or ("girls" in name):
                item_mapped, size_mapped = Command.itemMap(name)
                print(item_mapped + " " + size_mapped)
                item_new = Item.objects.get(name = item_mapped + " " + size_mapped)
                print(t.name, " qutity: ", t.quantity, "\n")
                print(item_new.name, " quantity: ", item_new.quantity, "\n")
                newQuantity = item_new.quantity + (t.quantity if t.quantity>0 else 0)
                item_new.quantity = newQuantity
                item_new.save()         

    def _update_item_transaction(self):
        for ins in ItemTransaction.objects.all():
            itemOld = Item.objects.get(id = ins.item_id)
            if ("boys" in itemOld.name) or ("girls" in itemOld.name):
                item_mapped, size_mapped = Command.itemMap(itemOld.name)
                item_new = Item.objects.get(name = item_mapped + " " + size_mapped)
                ins.item_id = item_new.id
                ins.save()
        print("transaction updated.\n")

            
    def handle(self, *args, **options):
        self._add_outdated()
        self._add_newitems()
        self._update_newitems()
        self._update_item_transaction()