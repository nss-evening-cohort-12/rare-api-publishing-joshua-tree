from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rareapi.models import Subscription, RareUser


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['id', 'created_on', 'ended_on', 'follower_id', 'author_id']

class SubscriptionViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk=None):
    # Get subscriptions by pk (this is necessary for HyperLinkedSerializers)

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

        subscription = Subscription()
        subscription.created_on = timezone.now()
        subscription.ended_on = ''
        subscription.follower_id = follower_id
        subscription.author_id = request.data['author_id']

        try:
            subscription.save()
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
