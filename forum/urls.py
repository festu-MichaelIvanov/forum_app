from django.urls import path, include

from rest_framework.routers import DefaultRouter

from forum_app.rest_views import CommentViewSet, MaterialViewSet

router = DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
