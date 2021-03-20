from django.contrib import admin
from .models import TodoItem,NoteItem

admin.site.register(TodoItem)
admin.site.register(NoteItem)
