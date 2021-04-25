
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
  name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Full Name')
  # created_at = models.DateTimeField(default=timezone.now)
  # USE Family.child_set OR .children TO GET QuerySet<Child>

  @property
  def child_names(self):
    return ','.join(map(lambda c: c.name, self.children.all()))
  
  def __str__(self):
    if self.fname: 
      return "{}, {}".format(self.lname, self.fname)
    return "{}".format(self.lname)
  
  class Meta:
    verbose_name_plural = "families"

  def save(self, *args, **kwargs):
    self.name = self.__str__()
    super(Family, self).save(*args, **kwargs)


class Child(models.Model): 
  name = models.CharField(max_length=50, blank=False, null=False)
  family = models.ForeignKey(Family, related_name='children', on_delete=models.CASCADE, blank=False, null=False)

  def __str__(self):
    return "{}".format(self.name)
  
  class Meta:
    verbose_name_plural = "children"

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

class Item(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True) # CASCADE - deletes all items if a Category is deleted
  name = models.CharField(max_length=50, blank=False, null=False, unique=True)
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
  datetime = models.DateTimeField(default=timezone.now)
  items = models.ManyToManyField(ItemTransaction, blank=False)

  def getValue(self):
    val = 0
    for tx in self.items.all().select_related("item"):
      val += 0 if tx.item.price is None else (tx.item.price * tx.quantity)
    return val

  def __str__(self):
    return "({}, {})".format(self.datetime, self.in_items)

  @property
  def in_items(self):
        return ", ".join([str(i) for i in self.items.all()])
  
  class Meta:
    ordering = ['-datetime']

class Checkout(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
  family = models.ForeignKey(Family, on_delete=models.PROTECT, blank=True, null=True)
  items = models.ManyToManyField(ItemTransaction, blank=False)
  datetime = models.DateTimeField(default=timezone.now)
  notes = models.CharField(max_length=500, blank=True, null=True)

  def getValue(self):
    val = 0
    for tx in self.items.all().select_related("item"):
      val += 0 if tx.item.price is None else (tx.item.price * tx.quantity)
    return val

  def __str__(self):
    return "({}, {})".format(self.family, self.out_items)
  
  @property
  def out_items(self):
        return ", ".join([str(i) for i in self.items.all()])
  
  class Meta:
    ordering = ['-datetime']
