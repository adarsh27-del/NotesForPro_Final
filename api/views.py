# api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from notes.models import Note
from tasks.models import Task
from whiteboard.models import Whiteboard
from ai_tools.models import AIResult
from graph.models import Graph
from games.models import GameScore
from mindmap.models import MindMap
from .serializers import (
    NoteSerializer,
    TaskSerializer,
    WhiteboardSerializer,
    UserMinimalSerializer,
    AIToolResultSerializer,
    GraphSerializer,
    GameScoreSerializer,
    MindMapSerializer,
    RegisterSerializer
)

    
class CustomAuthToken(ObtainAuthToken):
    """
    Login and get authentication token + basic user info
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "status": "success",
            "token": token.key,
            "user": UserMinimalSerializer(user).data
        })

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "status": "success",
                "message": "Account created successfully!",
                "username": user.username
            }, status=201)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)
    
            
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WhiteboardViewSet(viewsets.ModelViewSet):
    serializer_class = WhiteboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Whiteboard.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ──── AI Tools ────
class AIToolResultViewSet(viewsets.ModelViewSet):
    serializer_class = AIToolResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIResult.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ──── Graph Creator ────
class GraphViewSet(viewsets.ModelViewSet):
    serializer_class = GraphSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Graph.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ──── Mind Map ────
class MindMapViewSet(viewsets.ModelViewSet):
    serializer_class = MindMapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MindMap.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ──── Games ────
class GameScoreViewSet(viewsets.ModelViewSet):
    serializer_class = GameScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GameScore.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)