from django.urls import path
from .views import UserCreateView
from django.contrib.auth.views import LogoutView


app_name = 'accounts'


urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    #path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

