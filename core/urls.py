"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import RedirectView

from bee.views import RegisterFormView, UserProfile, UpdateProfile

urlpatterns = [
    path("", RedirectView.as_view(url="/bee/")),
    path('admin/', admin.site.urls),
    path('bee/', include('bee.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterFormView.as_view(), name="register"),
    path('accounts/my_profile/', UserProfile.as_view(), name="profile"),
    path('accounts/update_profile/', UpdateProfile.as_view(), name="update_profile"),


]
