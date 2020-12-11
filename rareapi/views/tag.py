"""View module for handling requests about tags"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Tag

class Tags(ViewSet):
    """Rare tags"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized tag instance
        """


        tag = Tag()
        tag.label = request.data["label"]

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag instance
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to tags resource

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments:
        serializer type
    """

    class Meta:
        model = Tag
        url = serializers.HyperlinkedIdentityField(
            view_name='tag',
            lookup_field='id'
        )
        fields = ('id', 'url', 'label')
