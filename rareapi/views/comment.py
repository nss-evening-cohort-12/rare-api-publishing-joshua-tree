"""View module for handling requests about comments"""
from rareapi.models.post import Post
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, RareUser

class Comments(ViewSet):
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
        comment.created_on = request.data["createdOn"]

        post = Post.objects.get(pk=request.data["postId"])
        comment.post = post
        
        comment.author = author

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment instance
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to comments resource

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a comment

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     comment = Comment.objects.get(pk=pk)
    #     comment.label = request.data["label"]
    
    #     comment.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments

    Arguments:
        serializer type
    """

    class Meta:
        model = Comment
        url = serializers.HyperlinkedIdentityField(
            view_name='comment',
            lookup_field='id'
        )
        fields = ('id', 'url', 'content', 'subject', 'author', 'post', 'created_on')
        depth = 1
        
class CommentUserSerializer(serializers.ModelSerializer):
    """JSON serializer for commenter's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CommentRareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for commenter's rare user"""
    user = CommentUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['user', 'bio', 'display_name', 'profile_image_url']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'publication_date', 'image_url', 'content', 'approved', 'rare_user', 'category')
        depth = 1
