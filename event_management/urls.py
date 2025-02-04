from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import no_permission, home_page
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home_page'),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('no_permission/', no_permission, name='no_permission'),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
