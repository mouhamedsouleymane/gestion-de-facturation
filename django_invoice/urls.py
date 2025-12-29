from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static

from fact_app.spa_views import spa_index

urlpatterns = [
    path('admin/', admin.site.urls),

    # JSON API consumed by AngularJS
    path('api/', include('fact_app.api_urls')),

    # SPA entrypoint (served for all non-admin routes)
    re_path(r'^.*$', spa_index),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', spa_index, name='spa_index'), # For language prefix
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
