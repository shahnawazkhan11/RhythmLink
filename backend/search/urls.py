from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = 'search'

urlpatterns = [
    path('', include(router.urls)),
    path('autocomplete/', views.autocomplete_search, name='autocomplete'),
]