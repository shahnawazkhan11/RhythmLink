from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'venues', views.VenueViewSet)
router.register(r'event-types', views.EventTypeViewSet)

app_name = 'events'

urlpatterns = [
    path('', include(router.urls)),
]