from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status, viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import RareUser
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # JSON Serializer for User
    
    class Meta:
        model = RareUser
        fields = ['id', 'user', 'bio', 'display_name', 'profile_image_url']

class UsersViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        # Get posts by pk (this is necessary for HyperLinkedSerializers)

        try:
            post = RareUser.objects.get(pk=pk)
            serializer = UserSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request, pk=None):
        # Get all posts
        
        users = RareUser.objects.all()

        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
