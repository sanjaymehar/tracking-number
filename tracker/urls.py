from django.urls import path
from .views import generate_tracking_number_view

urlpatterns = [
    path('next-tracking-number/', generate_tracking_number_view),
]
