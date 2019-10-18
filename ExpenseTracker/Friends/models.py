from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Request(models.Model):
    SentBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserID_SentBy')
    SentTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserID_SentTo')
    Status = models.BooleanField(default=False)
    DateTimeSent = models.DateTimeField(default=datetime.now,blank =True)
    def __str__(self):
        return str(self.SentTo)

class Friend(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserID_MyID')
    FriendID =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserID_FriendID')
    FriendSince = models.DateTimeField(default=datetime.now,blank =True)
    def __str__(self):
        return str(self.UserID)