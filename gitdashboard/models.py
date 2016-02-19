from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

# Create your models here.

class Repo(models.Model):
  rname = models.CharField(max_length=40) 
  created_date = models.DateTimeField(default=timezone.now)
  branch = models.ForeignKey('Branch')
  group = models.ForeignKey(Group)

  def __str__(self):
    return str(self.rname)

class Branch(models.Model):
  bname = models.CharField(max_length=40)
  created_date = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return self.bname
