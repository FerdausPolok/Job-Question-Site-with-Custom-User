from django import template
from user_profile.models import Profile


register = template.Library()


@register.simple_tag()
def get_profile_id(user_id=None):
    profile_obj = Profile.objects.filter(user_id=user_id).first()
    return profile_obj.id
