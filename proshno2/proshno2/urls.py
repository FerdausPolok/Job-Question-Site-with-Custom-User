from django.contrib import admin
from django.urls import path, include
from post import urls as post_urls
from django.contrib.auth import urls as auth_urls
from accounts import urls as my_user_urls
from django.conf import settings
from user_profile import urls as user_profile_urls
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include(post_urls, namespace='post')),
    #path('account/', include(auth_urls)),
    path('account/', include(my_user_urls, namespace='accounts')),
    path('', include(user_profile_urls, namespace='user_profile')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

