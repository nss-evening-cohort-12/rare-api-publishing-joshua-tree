from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post

class PostViewSet(ViewSet):

    def get_queryset(self):
        all_posts = Post.objects.all()
        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            user_posts = all_posts.filter()
        
        return user_posts
