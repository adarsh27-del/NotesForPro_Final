from django.urls import path
from . import views

app_name = "mindmap"

urlpatterns = [
    path('', views.generator, name='generator'),
    path('generate/', views.generate, name='generate'),
]