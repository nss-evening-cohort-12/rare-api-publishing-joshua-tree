import os
import base64
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.http import HttpResponseServerError
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser, Tag
from rareapi.serializers import PostCreateSerializer

class PostSerializer(serializers.ModelSerializer):
    # JSON Serializer for Post

    model = Category
    model = Tag
    
    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'publication_date', 'image_url', 'content', 'approved', 'rare_user', 'category', 'tags']
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

    def create(self, request):
        # Create a new post

        rare_user = RareUser.objects.get(user=request.auth.user)

        # Format post image
        format, imgstr = request.data['image_url'].split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')

        post = Post()
        post.title = request.data['title']
        post.publication_date = timezone.now()
        post.image_url = image_data
        #post.image_url = request.data['image_url']
        post.content = request.data['content']
        post.approved = request.data['approved']
        post.rare_user = rare_user

        category = Category.objects.get(pk=request.data['category'])
        post.category = category
        #tagsData = request.data['tags']
        #for tag in  tagsData:
        #    post.tags.add(tagsData)
        #post.tags.set(request.data['tags'])

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            tagsData = request.data['tags']
            for tag in  tagsData:
                tagId = Tag.objects.get(pk=tag)
                post.tags.add(tagId)
            post.save()
            serializer = PostCreateSerializer(post, context={'request': request})
            
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        # Get all posts
        
        posts = Post.objects.all()

        user_id = self.request.query_params.get('user_id', None)

        if user_id is not None:
            posts = posts.filter(rare_user__id=user_id)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @receiver(models.signals.post_delete, sender=Post)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        # Deletes file from filesystem when corresponding `Post` object is deleted.

        if instance.image_url:
            if os.path.isfile(instance.image_url.path):
                os.remove(instance.image_url.path)


    def update(self, request, pk=None):
        # Update post

        rare_user = RareUser.objects.get(user=request.auth.user)

        # Format post image
        format, imgstr = request.data['image_url'].split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')

        post = Post.objects.get(pk=pk)
        post.title = request.data['title']
        post.publication_date = request.data['publication_date']
        post.image_url = image_data
        #post.image_url = request.data['image_url']
        post.content = request.data['content']
        post.approved = request.data['approved']
        post.rare_user = rare_user

        category = Category.objects.get(pk=request.data['category'])
        post.category = category
        post.tags.set(request.data["tags"])
        post.save()
        #tagsData = request.data['tags']
        #for tag in  tagsData:
            #tagId = Tag.objects.get(pk=tag)
            #post.tags.add(tagId)
        #post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    @receiver(models.signals.pre_save, sender=Post)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        # Deletes old file from filesystem when corresponding `Post` object is updated with new file.

        if not instance.pk:
            return False

        try:
            old_file = Post.objects.get(pk=instance.pk).image_url
        except Post.DoesNotExist:
            return False

        new_file = instance.image_url
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
