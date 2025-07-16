"""jumcms URL Configuration

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
from django.urls import path, include
from users.controllers import home

from django.conf import settings
from django.conf.urls.static import static
from users.controllers import log_in

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("users/", include("users.urls")),
    path("appointments/", include("appointments.urls")),
    path("medical_test/", include("medical_tests.urls")),
    path("blogs/", include("blogs.urls")),
    path("medicines/", include("medicines.urls", "medicines")),
    path("accounts/login/", log_in, name="default-log-in"),
    path("certifications/", include("certifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
