from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from user_profile.models import Profile
from django.shortcuts import reverse

User = get_user_model()


def get_profile_id(self):
    pass


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'accounts/user_login.html'

    def get_success_url(self, *args, **kwargs):
        profile_obj = Profile.objects.get(user_id=self.request.user.id)
        return reverse_lazy('user_profile:profile_detail', kwargs={'pk': profile_obj.id})
