
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import Client, Project
from .serializers import ClientCreateUpdateSerializer, ClientDetailSerializer, ClientListSerializer, ClientUpdateResponseSerializer, ProjectCreateResponseSerializer, ProjectListSerializer, ProjectSerializer, UserSerializer


# -------Client API View
class ClientAPIView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            client = get_object_or_404(Client, pk=pk)
            serializer = ClientDetailSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)

        clients = Client.objects.all()
        serializer = ClientListSerializer(clients, many=True)
        return Response({'message':'Client list', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        created_by_id = request.data.get("created_by")

        if not created_by_id:
            return Response({"error": "created_by field is required"},status=status.HTTP_400_BAD_REQUEST)

        try:
            created_by_user = User.objects.get(pk=created_by_id)
        except User.DoesNotExist:
            return Response({"error": f"User with id {created_by_id} does not exist."},status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save(created_by=created_by_user)
            return Response(ClientCreateUpdateSerializer(client).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk):
        try:
            try:
                client = Client.objects.get(pk=pk)
            except Client.DoesNotExist:
                return Response({"error": f"Client with id {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND) 
        
            serializer = ClientCreateUpdateSerializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                client = serializer.save()
                response_serializer = ClientUpdateResponseSerializer(client)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def delete(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response({"message": "Client deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
# --------project API view
class ProjectAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, client_id):
        created_by_id = request.data.get('created_by')
        if not created_by_id:
            return Response({"error": "created_by field is required"},status=status.HTTP_400_BAD_REQUEST)

        try:
            created_by = User.objects.get(pk=created_by_id)
        except User.DoesNotExist:
            return Response({"error": f"User with id {created_by_id} does not exist"},status=status.HTTP_404_NOT_FOUND)

        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            return Response({"error": f"Client with id {client_id} does not exist"},status=status.HTTP_404_NOT_FOUND)

        project_name = request.data.get("project_name")
        user_ids = [user.get("id") for user in request.data.get("user", [])]

        if project_name and user_ids:
            existing_projects = Project.objects.filter(
                client=client,
                project_name=project_name,
                user__id__in=user_ids
            ).distinct()

            if existing_projects.exists():
                return Response({"error": "Given project already assigned to the user"},status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(client=client, created_by=created_by)
            response_serializer = ProjectCreateResponseSerializer(project)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

# --------Add user API view
class RegisterUserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"id": user.id, "username": user.username, "email": user.email}, status=status.HTTP_201_CREATED)
