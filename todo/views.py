# from django.db.models.query import RawQuerySet
from django.db.models.query import InstanceCheckMeta
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from .models import TodoItem, NoteItem
from django.contrib.auth.decorators import login_required
from .forms import TodoItemForm, NoteItemForm
from django.utils import timezone


# without auth views
# ,,,,,,,,,,,START,,,,,,,,,,,,,,,

def about(request):
   return render(request, 'about.html')

def home(request):
   # if User:
   #    todos = TodoItem.objects.filter(user = request.user, datecompleted__isnull = True).count()
   #    completed = TodoItem.objects.filter(user = request.user, datecompleted__isnull = False).count()
   #    notes = NoteItem.objects.filter(user = request.user).count()

   #    return render(request, 'home.html',{'todos':todos,'completed':completed,'notes':notes})   
   # else:
   return render(request, 'home.html')   


def userhome(request):
   todos = TodoItem.objects.filter(user = request.user, datecompleted__isnull = True).count()
   completed = TodoItem.objects.filter(user = request.user, datecompleted__isnull = False).count()
   notes = NoteItem.objects.filter(user = request.user).count()

   return render(request, 'userhome.html',{'todos':todos,'completed':completed,'notes':notes})   


#````````````END``````````````````

# views for authentication url 
# ,,,,,,,,,,,START,,,,,,,,,,,,,,,

def signupuser(request):
   if request.method == 'GET':
      return render(request, 'auths/signupuser.html', {'form':UserCreationForm()})

   else:
      #creating a new user object
      if request.POST['password1'] ==  request.POST['password2']:
         try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('todo')

         except IntegrityError:
            return render(request, 'auths/signupuser.html', {'form': UserCreationForm(), 'error':'This username has already been taken choose a unique one for you.'})

      else:
         return render(request, 'auths/signupuser.html', {'form':UserCreationForm(), 'error': 'password did not match'})

def loginuser(request):
   if request.method == 'GET':
      return render(request, 'auths/loginuser.html', {'form':AuthenticationForm()})

   else:
      #creating login use object
      user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
      if user is None:
         return render(request, 'auths/loginuser.html', {'form':AuthenticationForm(), 'error':'Username & password did not match'})

      else:
         login(request, user)
         return redirect('userhome')

def logoutuser(request):
   if request.method == 'POST':
      logout(request)
      return redirect('home')

#````````````END``````````````````

# Views for Todo After authenticated
# ,,,,,,,,,,,START,,,,,,,,,,,,,,,,,

@login_required
def createtodo(request):
   if request.method == 'GET':
      return render(request, 'todo/createtodo.html', {'form': TodoItemForm()})
   else:
      try:
         form = TodoItemForm(request.POST)
         newtodo = form.save(commit=False)
         newtodo.user = request.user
         newtodo.save()
         return redirect('todo')

      except ValueError:
         return render(request, 'todo/createtodo.html', {'form': TodoItemForm(),'error':'Atleast title is required !'})

@login_required
def todoView(request,id=None):
   all_todo_items = TodoItem.objects.filter(user = request.user, datecompleted__isnull = True)
   return render(request, 'todo/todo.html', {'all_items':all_todo_items})

@login_required
def completedTodos(request,id=None):
   all_todo_items = TodoItem.objects.filter(user = request.user, datecompleted__isnull = False).order_by("-datecompleted")
   return render(request, 'todo/completedTodos.html', {'all_items':all_todo_items})

@login_required
def addTodo(request):
   new_item = TodoItem(content = request.POST['content'])
   new_item.save()
   return HttpResponseRedirect('/todo')

@login_required
def deleteTodo(request,todo_id):
   item_to_delete = TodoItem.objects.get(id=todo_id)
   item_to_delete.delete()
   return HttpResponseRedirect('/todo')

@login_required
def updateTodo(request, todo_id):
   todo = get_object_or_404(TodoItem, pk=todo_id, user = request.user)
   if request.method =='GET':
      form = TodoItemForm(instance=todo)
      return render(request, 'todo/updateTodo.html', {'todo':todo, 'form':form})
   else:
      try:
         form = TodoItemForm(request.POST,instance=todo)
         form.save()
         return redirect('todo')

      except ValueError:
         return render(request, 'todo/updateTodo.html', {'todo':todo,'form':form,'error':'Bad data !'})

@login_required
def completeTodo(request, todo_id):
   todo = get_object_or_404(TodoItem, pk=todo_id, user = request.user)
   if request.method =='POST':
      todo.datecompleted = timezone.now()
      todo.save()
      return redirect('todo')

#````````````END``````````````````

# Views For Note
# ,,,,,,,,,,,START,,,,,,,,,,,,,,,,,

@login_required
def createnote(request):
   if request.method == 'GET':
      return render(request, 'note/createnote.html', {'form': NoteItemForm()})
   else:
      try:
         form = NoteItemForm(request.POST)
         newNote = form.save(commit=False)
         newNote.user = request.user
         newNote.save()
         return redirect('note')

      except ValueError:
         return render(request, 'note/createnote.html', {'form': NoteItemForm(),'error':'Atleast title is required !'})

@login_required
def noteView(request):
   all_note_items = NoteItem.objects.filter(user = request.user)
   return render(request, 'note/note.html', {'all_items':all_note_items})

@login_required
def addNote(request):
   new_item = NoteItem(content = request.POST['content'])
   new_item.save()
   return HttpResponseRedirect('/note')

@login_required
def deleteNote(request,note_id):
   item_to_delete = NoteItem.objects.get(id=note_id)
   item_to_delete.delete()
   return HttpResponseRedirect('/note')

#````````````END``````````````````
