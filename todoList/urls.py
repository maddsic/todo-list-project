from django.urls import path
from .views import TodoList, TodoDetail, TodoCreate, TodoUpdate, TodoDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
# from django.views.generic import TemplateView


urlpatterns = [
    # Registration Views
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(),  name='register'),

    # Templates views
    path('',  TodoList.as_view(), name='todo-list'),
    path('todo/<int:pk>',  TodoDetail.as_view(), name='todo-detail'),
    path('todo-create/',  TodoCreate.as_view(), name='todo-create'),
    path('todo-update/<int:pk>',  TodoUpdate.as_view(), name='todo-update'),
    path('todo-delete/<int:pk>', TodoDelete.as_view(), name='todo-delete'),


]
