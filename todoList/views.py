from django.shortcuts import redirect

from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Todo


# By default django looks for templates with the prefix of the className eg. todo_list.html but it can be changed by using the template_name and then pointing to the templates folder.

# Create your views here.


class CustomLoginView(LoginView):
    # Creating our Login view
    template_name = 'todoList/registration/login.html'
    fields = '__all__'
    redirect_auth_user = True

    def get_success_url(self):
        return reverse_lazy('todo-list')


class RegisterPage(FormView):
    # This is our registration page
    template_name = 'todoList/registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            # logged the user in automatically using the login function by passing in the user & form
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todo-list')
        return super(RegisterPage, self).get(*args, **kwargs)


class TodoList(LoginRequiredMixin, ListView):
    # This view is responsible for rendering all our todos from the DB
    model = Todo
    context_object_name = 'todos'
    template_name = 'todoList/todolist.html'

    def get_context_data(self, **kwargs):
        # Each user gets there own data... the above method returns an obj of data that we can use or alter in various ways. Here we are filtering the todos based on each user  and then counting the numbe of incompleted todos for each user.
        context = super().get_context_data(**kwargs)
        context['todos'] = context['todos'].filter(user=self.request.user)
        context['count'] = context['todos'].filter(
            completed=False).count()

        # implementing our search functionality
        search_input = self.request.GET.get('search_box') or ''
        if search_input:
            context['todos'] = context['todos'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input

        return context


class TodoDetail(LoginRequiredMixin, DetailView):
    # This view is responsible for each todos detail view.
    model = Todo
    context_object_name = 'todo'
    template_name = 'todoList/todo.html'


class TodoCreate(LoginRequiredMixin, CreateView):
    # This view is responsible creating a new Todo and adds them to the DB
    model = Todo
    fields = ['title', 'description', 'completed']
    template_name = 'todoList/todoform.html'
    success_url = reverse_lazy('todo-list')


def form_valid(self, form):
    # Auto detecting the current user for creating a new todo
    form.instance.user = self.request.user
    return super(TodoCreate, self).form_valid(form)


class TodoUpdate(LoginRequiredMixin, UpdateView):
    # Update view... for editing our todos
    model = Todo
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('todo-list')
    template_name = 'todoList/todoupdate.html'


class TodoDelete(LoginRequiredMixin, DeleteView):
    # To delete a todo
    model = Todo
    context_object_name = 'todo'
    success_url = reverse_lazy('todo-list')
    template_name = 'todoList/todoDelete.html'
