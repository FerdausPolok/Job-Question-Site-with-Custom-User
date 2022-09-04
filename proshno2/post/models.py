from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('hidden', 'Hidden')
    )

    companyName = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'post_author')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('post:post_details', args=(self.id,))

    def __str__(self):
        ret_str = "'"+self.position+"'" + " at " + self.companyName
        return ret_str

class PostComment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment_post')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now = True)
    up_vote = models.IntegerField(default=0)
    down_vote= models.IntegerField(default=0)


    def __str__(self):
        return self.body[:30]
