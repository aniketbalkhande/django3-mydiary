from django.db import models
from django.contrib.auth.models import User



class TodoItem(models.Model):
   user = models.ForeignKey(User, on_delete=models.PROTECT,null=True)
   title = models.CharField(max_length=255,blank=False, null=False)
   description = models.TextField(blank=True)
   dateadded = models.DateTimeField(auto_now_add=True)
   datecompleted = models.DateTimeField(null=True, blank=True)
   important = models.BooleanField(null=False)

   def __str__(self):
      return 'User: {} =>Todo: {}'.format(self.user, self.title)



class NoteItem(models.Model):
   user = models.ForeignKey(User, on_delete=models.PROTECT,null=True)
   title = models.CharField(max_length=255,blank=False, null=False)
   description = models.TextField(blank=True)
   dateadded = models.DateTimeField(auto_now_add=True)
   important = models.BooleanField(null=False)

   def __str__(self):
      return 'User: {} =>Note: {}'.format(self.user, self.title)


