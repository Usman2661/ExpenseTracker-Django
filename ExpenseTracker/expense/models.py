from django.db import models
from  django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Expenses(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Amount = models.IntegerField(blank=False)
    Catagory = models.CharField(max_length=200 , blank=False)
    Contents=models.TextField(max_length=200)
    Notes=models.TextField(max_length=200)
    Date_Time = models.DateTimeField(default=datetime.now,blank =True)
    def __str__(self):
        return self.Catagory

class Catagory(models.Model):
    User_ID = models.IntegerField(blank=False, default=0)
    Name = models.CharField(max_length=200)
    def __str__(self):
        return self.Name