from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

app_name = 'customers'

urlpatterns = [
    path('', include(router.urls)),
    path('book/', views.BookingCreateView.as_view(), name='create-booking'),
    path('my-bookings/', views.CustomerBookingsView.as_view(), name='my-bookings'),
]