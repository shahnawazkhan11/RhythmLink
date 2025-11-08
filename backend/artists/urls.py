from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'artists', views.ArtistViewSet)
router.register(r'genres', views.GenreViewSet)

app_name = 'artists'

urlpatterns = [
    path('', include(router.urls)),
]