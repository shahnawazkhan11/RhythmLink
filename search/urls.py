from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = 'search'

urlpatterns = [
    path('', include(router.urls)),
    path('autocomplete/', views.AutocompleteView.as_view(), name='autocomplete'),
    path('popular/', views.PopularSearchesView.as_view(), name='popular-searches'),
]