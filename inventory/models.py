
# IMPORTS 

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# MODELS 

class Family(models.Model):
  name = models.CharField(max_length=50, blank=False, null=False)
  # first_seen = models.DateTimeField(default=datetime.now)

class Category(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)
	
class Item(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True) # CASCADE - deletes all items if a Category is deleted
  name = models.CharField(max_length=50, blank=False, null=False)
  price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 
  quantity = models.IntegerField(default=0)

class ItemTransaction(models.Model):
  item = models.ForeignKey(Item, on_delete=models.PROTECT, blank=True, null=True)
  quantity = models.IntegerField(default=0)
  
class Checkin(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  datetime = models.DateTimeField(default=datetime.now)
  items = models.ManyToManyField(ItemTransaction, blank=False)

class Checkout(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  family = models.ForeignKey(Family, on_delete=models.PROTECT, blank=True, null=True)
  items = models.ManyToManyField(ItemTransaction, blank=False)
  datetime = models.DateTimeField(default=datetime.now)
