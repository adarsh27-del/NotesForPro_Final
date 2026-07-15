from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='list'),
    path('new/', views.note_detail, name='new'),
    path('<int:note_id>/', views.note_detail, name='detail'),
    path('save/', views.note_save, name='save'),
    path('delete/<int:note_id>/', views.note_delete, name='delete'),
]