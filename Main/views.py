from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import todo
from django.views import View
from django.db import transaction
from .forms import PositionForm

class Login(LoginView):
  template_name = 'Main/login.html'
  fields = '__all__'
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('todo')

class RegisterPage(FormView):
  template_name = 'Main/register.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('todo')

  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(RegisterPage, self).form_valid(form)

  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('todo')
    return super(RegisterPage, self).get(*args, **kwargs)
    

class ToDoList(LoginRequiredMixin, ListView):
  model = todo
  context_object_name = 'todo'
  template_name = 'Main/list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['todo'] = context['todo'].filter(user=self.request.user)
    context['count'] = context['todo'].filter(complete=False).count()
    
    search_input = self.request.GET.get('search-area') or ''
    if search_input:
      context['todo'] = context['todo'].filter(title__contains=search_input)
    context['search_input'] = search_input
    return context


class ToDoDetail(LoginRequiredMixin,DetailView):
  model = todo
  context_object_name = 'todos'
  template_name = 'Main/detail.html'

class ToDoCreate(LoginRequiredMixin,CreateView):
  model = todo
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('todo')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(ToDoCreate, self).form_valid(form)

class ToDoUpdate(LoginRequiredMixin,UpdateView):
  model = todo
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('todo')

class DeleteView(LoginRequiredMixin,DeleteView):
  model = todo
  context_object_name = 'todos'
  success_url = reverse_lazy('todo')
  template_name = 'Main\delete.html'
  def get_queryset(self):
    owner = self.request.user
    return self.model.objects.filter(user=owner)
  
class TodoReorder(View):
    def post(self, request):
      form = PositionForm(request.POST)

      if form.is_valid():
          positionList = form.cleaned_data["position"].split(',')

          with transaction.atomic():
              self.request.user.set_todo_order(positionList)

      return redirect(reverse_lazy('todo'))

