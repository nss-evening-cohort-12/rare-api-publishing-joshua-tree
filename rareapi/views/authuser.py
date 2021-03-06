from django.contrib.auth.models import User
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rareapi.models import RareUser

class UserSerializer(serializers.ModelSerializer):
    # JSON Serializer for User
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'password', 'is_active']

class AuthUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):

        queryset = User.objects.all()
        status = self.request.query_params.get('is_active', None)
        staff = self.request.query_params.get('is_staff', None)
        if status is not None:
            queryset = queryset.filter(is_active=status)
        elif staff is not None:
            queryset = queryset.filter(is_staff=staff)
        return queryset
