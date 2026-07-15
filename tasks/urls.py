# tasks/urls.py
from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('',               views.task_board,     name='board'),
    path('create/',        views.task_create,    name='create'),
    path('<int:task_id>/update/', views.task_update,   name='update'),
    path('<int:task_id>/delete/', views.task_delete,   name='delete'),
    path('reorder/',       views.task_reorder,   name='reorder'),
]