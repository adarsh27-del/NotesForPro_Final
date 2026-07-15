# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

from notes.models import Note
from tasks.models import Task
from whiteboard.models import Whiteboard   # adjust name if you used different class name
from ai_tools.models import AIResult
from graph.models import Graph
from mindmap.models import MindMap
from games.models import GameScore

from django.core.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    password_confirm = serializers.CharField(write_only=True,style={'input_type': 'password'})
    email = serializers.EmailField(required=False, allow_blank=True,allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        email = validated_data.pop('email', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )
        return user


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = fields

        
class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        # We use these exact fields to match your database
        fields = ['id', 'title', 'content_json', 'content_html', 'created_at', 'updated_at', 'user']
        read_only_fields = ['created_at', 'updated_at', 'user']

    def to_internal_value(self, data):
        # This is the "Magic Fix" for saving. 
        # If the web sends 'content_json' as a string, we turn it into a Python object.
        import json
        if 'content_json' in data and isinstance(data['content_json'], str):
            try:
                data['content_json'] = json.loads(data['content_json'])
            except:
                pass
        return super().to_internal_value(data)


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'color',
            'created_at',
            'updated_at',
            'user',
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']


class WhiteboardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Whiteboard
        fields = [
            'id',
            'name',
            'image',
            'json_data',
            'created_at',
            'updated_at',
            'user',
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

class AIToolResultSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = AIResult
        fields = '__all__'
        read_only_fields = ['created_at']

class GraphSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Graph
        fields = '__all__'
        read_only_fields = ['created_at']

class MindMapSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = MindMap
        fields = '__all__'
        read_only_fields = ['created_at']

class GameScoreSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = GameScore
        fields = '__all__'
        read_only_fields = ['created_at']