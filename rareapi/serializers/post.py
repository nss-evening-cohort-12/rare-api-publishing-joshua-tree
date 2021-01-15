from rest_framework import serializers
from rareapi.models import Post

class PostCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'url', 'title', 'publication_date', 'image_url', 'content', 'approved', 'rare_user', 'category', 'tags')
