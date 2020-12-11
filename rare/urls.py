from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from rareapi.views import login_user, register_user
# from rareapi.views import logout_view
from django.conf.urls import include
from rest_framework import routers
from rareapi.views import CategoriesViewSet, Tags



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoriesViewSet, 'category')
router.register(r'tags', Tags, 'tag')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    # path('logout', logout_view),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
