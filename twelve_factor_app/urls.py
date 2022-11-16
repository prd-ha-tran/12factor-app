"""twelve_factor_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path

from .views import waiting_view, error_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("wait-me/", view=waiting_view),
    path("error/", view=error_view),
]

if settings.DISABLE_WHITENOSE:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.views import serve as serve_staticfiles

    urlpatterns += static(settings.STATIC_URL, view=serve_staticfiles)
