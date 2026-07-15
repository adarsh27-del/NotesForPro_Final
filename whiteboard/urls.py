from django.urls import path
from . import views

app_name = 'whiteboard'

urlpatterns = [
    path('', views.whiteboard_canvas, name='canvas'),
    
]