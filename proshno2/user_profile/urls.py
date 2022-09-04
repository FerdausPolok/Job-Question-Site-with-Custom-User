from django.urls import path
from user_profile.views import ProfileDetailView, profile_update_view


app_name = 'user_profile'


urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile-update/<int:profile_id>/', profile_update_view, name='profile_update'),
]
