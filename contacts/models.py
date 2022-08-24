from django.db import models
from datetime import datetime
from listings.models import Listing
# import  User
from django.contrib.auth.models import User


class Contact(models.Model):
  listing = models.CharField(max_length=200)
  listing_id = models.IntegerField()
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)
  user_id = models.IntegerField(blank=True)
  def __str__(self):
    return self.name


class Reservation(models.Model):

  farms = models.ForeignKey(Listing, related_name=("reservation_days"), on_delete=models.CASCADE)
  day = models.DateField(auto_now=False, auto_now_add=False)
  customer=models.ForeignKey(User,related_name=("customers"), on_delete=models.CASCADE)


  def __str__(self):
    self.day = str(self.day)
    return self.day
