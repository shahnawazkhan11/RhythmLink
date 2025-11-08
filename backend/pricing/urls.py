from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = 'pricing'

urlpatterns = [
    path('', include(router.urls)),
    path('tiers/<int:event_id>/', views.EventPriceTiersView.as_view(), name='event-price-tiers'),
    path('current-price/<int:event_id>/', views.CurrentPriceView.as_view(), name='current-price'),
]