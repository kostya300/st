from django.contrib import admin
from django.urls import path, include
from products.views import commonView
from django.conf.urls.static import static
from django.conf import settings
import mimetypes


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", commonView.as_view(), name="common"),
    path("prod/", include("products.urls", namespace="products")),
    path("users/", include("users.urls", namespace="users")),
    path("orders/", include("orders.urls", namespace="orders")),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    # Добавляем Debug Toolbar корректно — только через debug_toolbar_urls()
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns = [
        *debug_toolbar_urls(),  # ← Это уже включает нужные URL с namespace='djdt'
        *urlpatterns,
    ]

    # Регистрируем JS-тип (нужно только в Windows, но безопасно везде)
    mimetypes.add_type("application/javascript", ".js", True)

    # Статические и медиа-файлы
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
