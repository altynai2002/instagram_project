from django.urls import path, include

from account.views import UserProfile, follow
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('account/', include('account.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/follow/<option>', follow, name='follow'),
    path('accounts/', include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
