# graph/urls.py
from django.urls import path
from . import views

app_name = 'graph'

urlpatterns = [
    path('', views.graph_creator, name='creator'),
    path('generate/', views.graph_generate, name='generate'),
]