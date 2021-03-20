from django.db.models import fields
from django.forms import ModelForm
from .models import TodoItem, NoteItem

class TodoItemForm(ModelForm):
   class Meta:
      model = TodoItem
      fields = ['title','description','important']
      
class NoteItemForm(ModelForm):
   class Meta:
      model = NoteItem
      fields = ['title','description','important']
      