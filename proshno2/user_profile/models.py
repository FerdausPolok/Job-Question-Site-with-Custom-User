from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image


User = get_user_model()


class Profile(models.Model):
    image = models.ImageField(default='default.png', upload_to='profile_pics/')
    phone = models.CharField(max_length=30, blank=True)
    current_position = models.CharField(max_length=30, blank=True)
    current_company = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')

    def save(self, *args, **kwargs):
        super(Profile, self).save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)

    def __str__(self):
        return f"{self.user} Profile"

    def get_absolute_url(self):
        return reverse('user_profile:profile_detail', args=(self.id,))
