from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.utils import timezone
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rareapi.models import Subscription, RareUser


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['id', 'created_on', 'ended_on', 'follower_id', 'author_id']

class SubscriptionViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        # Get subscriptions by pk

        try:
            post = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        # Get all subscriptions
        
        posts = Subscription.objects.all()

        serializer = SubscriptionSerializer(
            posts, many=True, context={'request': request})
        
        return Response(serializer.data)


    def create(self, request):
        # Create a new subscription

        follower_id = RareUser.objects.get(user=request.auth.user)
        author_id = RareUser.objects.get(user=request.data['author_id'])

        subscription = Subscription()
        subscription.created_on = timezone.now()
        subscription.ended_on = request.data['ended_on']
        subscription.follower_id = follower_id
        subscription.author_id = author_id

        try:
            subscription.save()
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    
    def update(self, request, pk=None):
        # Update a subscription

        follower_id = RareUser.objects.get(user=request.auth.user)
        author_id = RareUser.objects.get(user=request.data['author_id'])
        created_on = request.data['created_on']
        ended_on = request.data['ended_on']
        
        subscription = Subscription.objects.get(pk=pk)
        subscription.follower_id = follower_id
        subscription.author_id = author_id

        if created_on is not None:
            subscription.created_on = request.data['created_on']
            subscription.ended_on = timezone.now()

        elif ended_on is not None:
            subscription.created_on = timezone.now()
            subscription.ended_on = request.data['ended_on']

        subscription.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
