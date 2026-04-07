from django.urls import path
from .views import ProfileView, upgrade_profile


urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('upgrade/', upgrade_profile, name='upgrade_profile')
]