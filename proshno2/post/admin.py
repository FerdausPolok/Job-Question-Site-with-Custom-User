from django.contrib import admin
from post.models import Post, PostComment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'position', 'body', 'author',)
    list_filter = ('status',)
    search_fields = ('companyName', 'position',)
    raw_id_fields = ('author',)

admin.site.register(PostComment)