from rareapi.models.category import Category
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post

class PostSerializer(serializers.ModelSerializer):
    # JSON Serializer for Post

    model = Category
    
    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'publication_date', 'image_url', 'content', 'approved', 'rare_user', 'category']
        depth = 1

class PostsViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        # Get posts by pk (this is necessary for HyperLinkedSerializers)

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request, pk=None):
        # Get all posts
        
        posts = Post.objects.all()

        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            posts = posts.filter(rare_user__id=user_id)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
