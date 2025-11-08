from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = 'analytics'

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/<int:event_id>/', views.EventDashboardView.as_view(), name='event-dashboard'),
    path('manager-dashboard/', views.ManagerDashboardView.as_view(), name='manager-dashboard'),
]