# games/urls.py
from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('typing/', views.typing_game, name='typing'),
    path('typing/check/', views.typing_game_check, name='typing_check'),
    path('chess/',  views.chess_game,  name='chess'),
]