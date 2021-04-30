
# IMPORTS 

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.utils import timezone

# MODELS 

class Family(models.Model):
  fname = models.CharField(max_length=50, blank=True, null=True, verbose_name='First Name')
  lname = models.CharField(max_length=50, blank=False, null=False,verbose_name='Last Name') # Only the last_name is required
  phone = PhoneNumberField(blank=True, null=True)
  displayName = models.CharField(max_length=150, blank=True, null=True, verbose_name='Family name and phone')
  # created_at = models.DateTimeField(default=timezone.now)
  # USE Family.child_set OR .children TO GET QuerySet<Child>
  
  def __str__(self):
    if self.fname: 
      return "{}, {}".format(self.lname, self.fname)
    return "{}".format(self.lname)
  
  class Meta:
    verbose_name_plural = "families"

  def save(self, *args, **kwargs):
    if self.phone:
      self.displayName = self.__str__() + f" : ({self.phone})"
    else:
      self.displayName = self.__str__() + " : (None)"
    super(Family, self).save(*args, **kwargs)

class Category(models.Model):
  name = models.CharField(max_length=50, blank=False, null=False, unique=True)

  # name being same as Item 'quantity' field is important so they can be sorted the same way
  @property
  def quantity(self):
    return Item.objects.filter(category=self).aggregate(models.Sum('quantity'))['quantity__sum']
  
  def __str__(self):
    return "{}".format(self.name)
  class Meta:
    verbose_name_plural = "categories"

class AgeRange(models.Model):
  low = models.CharField(max_length=50, blank=False, null=False, unique=True)
  high = models.CharField(max_length=50, blank=False, null=False, unique=True)
  def __str__(self):
    return "{} - {}".format(self.low, self.high)
  

class Item(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True) # CASCADE - deletes all items if a Category is deleted
  name = models.CharField(max_length=50, blank=False, null=False, unique=True)
  new_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
  used_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
  quantity = models.IntegerField(default=0)
  
  def __str__(self):
    return "{}".format(self.name)

class ItemTransaction(models.Model):
  item = models.ForeignKey(Item, on_delete=models.PROTECT, blank=True, null=True)
  quantity = models.IntegerField(default=0)
  is_new = models.BooleanField(default=False)

  def __str__(self):
    new_str = "New" if self.is_new else "Used"
    return "({}, {}, {})".format(self.item, self.quantity, new_str)

class Checkin(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  datetime = models.DateTimeField(default=timezone.now)
  items = models.ManyToManyField(ItemTransaction, blank=False)
  notes = models.CharField(max_length=500, blank=True, null=True)

  def getValue(self):
    val = 0
    for tx in self.items.all().select_related("item"):
      if tx.is_new:
        val += 0 if tx.item.new_price is None else (tx.item.new_price * tx.quantity)
      else:
        val += 0 if tx.item.used_price is None else (tx.item.used_price * tx.quantity)
    return val
  
  def getNewValue(self):
    '''
    Returns price assuming every item is new.
    '''
    val = 0
    for tx in self.items.all().select_related("item"):
      val += 0 if tx.item.new_price is None else (tx.item.new_price * tx.quantity)
    return val
  
  def getUsedValue(self):
    '''
    Returns price assuming every item is used.
    '''
    val = 0
    for tx in self.items.all().select_related("item"):
      val += 0 if tx.item.used_price is None else (tx.item.used_price * tx.quantity)
    return val

  def __str__(self):
    return "({}, {})".format(self.datetime, self.in_items)

  def notes_description(self): 
    return f"<b>Checkin #{self.id}:</b> " + self.notes + " <b>&nbsp;|&nbsp;</b> " + self.in_items if self.notes else None

  @property
  def in_items(self):
    def itemTransaction_checkin_str(it):
      '''
      Returns the item and quantity of an item transaction as a string, ignoring new/used.
      '''
      return "({}, {})".format(it.item, it.quantity)
    return ", ".join([itemTransaction_checkin_str(i) for i in self.items.all()])
  
  class Meta:
    ordering = ['-datetime']

class Checkout(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  datetime = models.DateTimeField(default=timezone.now)
  family = models.ForeignKey(Family, on_delete=models.PROTECT, blank=True, null=True)
  childName = models.CharField(max_length=50, blank=True, null=True, verbose_name='Child')
  ageRange = models.ForeignKey(AgeRange, on_delete=models.PROTECT, blank=True, null=True)
  items = models.ManyToManyField(ItemTransaction, blank=False)
  notes = models.CharField(max_length=500, blank=True, null=True)

  def getValue(self):
    val = 0
    for tx in self.items.all().select_related("item"):
      if tx.is_new:
        val += 0 if tx.item.new_price is None else (tx.item.new_price * tx.quantity)
      else:
        val += 0 if tx.item.used_price is None else (tx.item.used_price * tx.quantity)
    return val

  def __str__(self):
    return "({}, {})".format(self.family, self.out_items)
  
  def notes_description(self): 
    return f"<b>Checkout #{self.id}:</b> " + self.notes + " <b>&nbsp;|&nbsp;</b> " + self.out_items if self.notes else None

  @property
  def out_items(self):
        return ", ".join([str(i) for i in self.items.all()])
  
  class Meta:
    ordering = ['-datetime']
