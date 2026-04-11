from django.urls import path
from .views import (ProfileView, CategorySubscribe, 
    category_unsubscribe, upgrade_profile)


urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('upgrade/', upgrade_profile, name='upgrade_profile'),
    path('subscribe/', CategorySubscribe.as_view(), name='category_subscribe'),
    path('unsubscribe/<int:pk>/', category_unsubscribe, name='category_unsubscribe'),
]
