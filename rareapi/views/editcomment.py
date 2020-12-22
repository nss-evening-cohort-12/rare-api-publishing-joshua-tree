"""View module for handling requests about comments"""
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, RareUser, Post

class EditComments(ViewSet):
    """Rare comments"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized comment instance
        """

        author = RareUser.objects.get(user=request.auth.user)

        comment = Comment()
        comment.content = request.data["content"]
        comment.subject = request.data["subject"]
        comment.created_on = datetime.datetime.now()

        post = Post.objects.get(pk=request.data["post"])
        comment.post = post
        
        comment.author = author

        try:
            comment.save()
            serializer = EditCommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment instance
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = EditCommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to comments resource

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all()

        post = self.request.query_params.get('post', None)
        if post is not None:
            comments = comments.filter(post__id=post)

        serializer = EditCommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a comment

        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)
        comment.subject = request.data["subject"]
        comment.content = request.data["content"]
    
        comment.save()

        return Response('here is a string', status=status.HTTP_204_NO_CONTENT)


class EditCommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments

    Arguments:
        serializer type
    """

    class Meta:
        model = Comment
        fields = ('id', 'content', 'subject', 'author', 'post', 'created_on')
        depth = 1
        
class EditCommentUserSerializer(serializers.ModelSerializer):
    """JSON serializer for commenter's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditCommentRareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for commenter's rare user"""
    user = EditCommentUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['user', 'bio', 'display_name', 'profile_image_url']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'publication_date', 'image_url', 'content', 'approved', 'rare_user', 'category')
        depth = 1
