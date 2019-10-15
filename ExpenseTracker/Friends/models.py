from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Request(models.Model):
    SentBy = models.ForeignKey(User, on_delete=models.CASCADE)
    SentTo = models.ForeignKey(User, on_delete=models.CASCADE)
    Status = models.BooleanField(initial=False)
    DateTimeSent = models.DateTimeField(default=datetime.now,blank =True)
    def __str__(self):
        return self.Catagory

class Friend(models.Model):
    MyID = models.ForeignKey(User, on_delete=models.CASCADE)
    FriendID =  models.ForeignKey(User, on_delete=models.CASCADE)
    FriendSince = models.DateTimeField(default=datetime.now,blank =True)

    def __str__(self):
        return self.MyID