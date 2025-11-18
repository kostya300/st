from django.contrib import admin
from django.urls import path, include
from products.views import commonView
from django.conf.urls.static import static
from django.conf import settings
import mimetypes
from debug_toolbar.toolbar import debug_toolbar_urls  # Move import here

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", commonView.as_view(), name="common"),
    path("prod/", include("products.urls", namespace="products")),
    path("users/", include("users.urls", namespace="users")),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    # Инструментальная панель настройки
    urlpatterns = [
        *debug_toolbar_urls(),
        *urlpatterns,

    ]
    # Инструментальная панель настройки
    mimetypes.add_type("application/javascript", ".js", True)
    # Инструментальная панель настройки
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))

    # статические файлы
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
