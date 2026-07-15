# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    NoteViewSet,
    TaskViewSet,
    WhiteboardViewSet,
    CustomAuthToken,
    AIToolResultViewSet,
    GameScoreViewSet,
    GraphViewSet,
    MindMapViewSet,
    RegisterView
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'whiteboards', WhiteboardViewSet, basename='whiteboard')
router.register(r'ai-results', AIToolResultViewSet, basename='ai-result')
router.register(r'graphs', GraphViewSet, basename='graph')
router.register(r'mindmaps', MindMapViewSet, basename='mindmap')
router.register(r'game-scores', GameScoreViewSet, basename='game-score')

urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="api-register"),
    path('auth/login/', CustomAuthToken.as_view(), name='api-login'),
]