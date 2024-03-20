from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('', include('app_login.urls')),#sitenma de gerenciamento de força, posto, quadro

    path('admin/', admin.site.urls),
    path('', include('app_arq.urls')),#sistema de gerenciamento de certificados

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

