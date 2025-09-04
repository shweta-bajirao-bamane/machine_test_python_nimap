from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
#------Post method use to create project
class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user', [])
        project = Project.objects.create(**validated_data)

        user_ids = [u['id'] for u in user_data if 'id' in u]
        project.user.set(User.objects.filter(id__in=user_ids))

        return project


# ------All client list 
class ClientListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']
        
#------GET single client by id
class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'created_by', 'updated_at']
        
# ------Post & Put method use 
class ClientCreateUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'client_number', 'created_at', 'created_by']
        
# ------PUT method show response serializer client 
class ClientUpdateResponseSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']
        
# ------Post project only
class ProjectCreateResponseSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    user = UserSerializer(many=True, read_only=True)  # nested output
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'user', 'created_at', 'created_by']


# -------GET all project list 
class ProjectListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by']
