from django.urls import path

from .views import ClientAPIView, ProjectAPIView, RegisterUserView


urlpatterns = [
   path('client/', ClientAPIView.as_view(), name='client-list'),
   path('client/<int:pk>/', ClientAPIView.as_view(), name='client-detail'),
   
   path('project/', ProjectAPIView.as_view(), name='project-list'),
   path('project/<int:pk>/', ProjectAPIView.as_view(), name='project-detail'),
   path('clients/<int:client_id>/project/',ProjectAPIView.as_view(), name='project-add'),
   
   path('add-user/', RegisterUserView.as_view(), name='add-user-to-project'),
]