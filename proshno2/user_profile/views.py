from django.contrib.auth import get_user_model
from user_profile.models import Profile
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from post.models import Post
from user_profile.forms import ProfileUpdateForm
from accounts.forms import TemplateCustomUserChangeForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    template_name = 'user_profile/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)
        extra_context['post_queryset'] = Post.objects.filter(author=self.request.user)
        return extra_context

    def test_func(self):
        instance = self.get_object()
        return self.request.user == instance.user


@login_required
def profile_update_view(request, profile_id, *args, **kwargs):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        user_form = TemplateCustomUserChangeForm(instance=user, data=request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('user_profile:profile_detail', profile_id)

    else:
        user_form = TemplateCustomUserChangeForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'user_profile/edit_profile.html', context)
