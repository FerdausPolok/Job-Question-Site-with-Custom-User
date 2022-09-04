from django.contrib import admin
from django.urls import path, include
from post import urls as post_urls
from django.contrib.auth import urls as auth_urls
from accounts import urls as my_user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(post_urls, namespace='post')),
    #path('account/', include(auth_urls)),
    path('account/', include(my_user_urls, namespace='accounts')),


]
