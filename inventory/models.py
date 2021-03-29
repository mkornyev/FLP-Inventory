
# IMPORTS 

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# MODELS 

class Family(models.Model):
  name = models.CharField(max_length=50, blank=False, null=False)
  # first_seen = models.DateTimeField(default=datetime.now)

  def __str__(self):
    return "{}".format(self.name)

class Category(models.Model):
  name = models.CharField(max_length=50, blank=False, null=False)
  
  def __str__(self):
    return "{}".format(self.name)

class Item(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True) # CASCADE - deletes all items if a Category is deleted
  name = models.CharField(max_length=50, blank=False, null=False)
  price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 
  quantity = models.IntegerField(default=0)
  
  def __str__(self):
    return "{}".format(self.name)

class ItemTransaction(models.Model):
  item = models.ForeignKey(Item, on_delete=models.PROTECT, blank=True, null=True)
  quantity = models.IntegerField(default=0)

  def __str__(self):
    return "({}, {})".format(self.item, self.quantity)

class Checkin(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  datetime = models.DateTimeField(default=datetime.now)
  items = models.ManyToManyField(ItemTransaction, blank=False)

  def getValue(self):
    val = 0
    for tx in self.items.all().select_related("item"):
      val += (tx.item.price * tx.quantity)
    return val

  def __str__(self):
    return "({}, {})".format(self.datetime, self.in_items())
  def in_items(self):
        return ", ".join([str(i) for i in self.items.all()])
  
  class Meta:
    ordering = ['-datetime']

class Checkout(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  family = models.ForeignKey(Family, on_delete=models.PROTECT, blank=True, null=True)
  items = models.ManyToManyField(ItemTransaction, blank=False)
  datetime = models.DateTimeField(default=datetime.now)

  def getValue(self):
    val = 0
    for tx in self.items.all().select_related("item"):
      val += (tx.item.price * tx.quantity)
    return val

  def __str__(self):
    return "({}, {})".format(self.family, self.out_items())
  
  def out_items(self):
        return ", ".join([str(i) for i in self.items.all()])
  
  class Meta:
    ordering = ['-datetime']
