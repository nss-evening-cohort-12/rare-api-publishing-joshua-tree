from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rareapi.views import login_user, register_user
from rest_framework import routers
from rareapi.views import CategoriesViewSet, Tags, Comments, PostsViewSet, UsersViewSet, EditComments, AuthUserViewSet, SubscriptionViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoriesViewSet, 'category')
router.register(r'tags', Tags, 'tag')
router.register(r'comments', Comments, 'comment')
router.register(r'editcomments', EditComments, 'editcomment')
router.register(r'posts', PostsViewSet, 'post')
router.register(r'users', UsersViewSet, 'user')
router.register(r'authusers', AuthUserViewSet, 'authuser')
router.register(r'subscriptions', SubscriptionViewSet, 'subscription')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
