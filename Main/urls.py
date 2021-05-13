from django.urls import path
from .views import ToDoList, ToDoDetail, ToDoCreate, ToDoUpdate, DeleteView, Login, RegisterPage, TodoReorder
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('login/', Login.as_view(), name='login'),
  path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
  path('register/', RegisterPage.as_view(), name='register'),
  path('', ToDoList.as_view(), name='todo'),  #tasks
  path('todos/<int:pk>/', ToDoDetail.as_view(), name='todos'), #task
  path('todo_create/', ToDoCreate.as_view(), name='todo_create'),
  path('todo_update/<int:pk>/', ToDoUpdate.as_view(), 
  name='todo_update'),
  path('todo_delete/<int:pk>/', DeleteView.as_view(), name='todo_delete'),
  path('todo_reorder/', TodoReorder.as_view(), name='todo_reorder'),

]