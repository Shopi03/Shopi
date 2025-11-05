"""
URL configuration for Shopi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# fichier : SHOPI/urls.py

from django.contrib import admin
from django.urls import path, include

# Pour gérer les fichiers médias (images de profil)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclure les URLS de l'application Partenaire
    path('partenaire/', include('Partenaire.urls')),  # toutes les URLs de Partenaire
    path('livreur/', include('Livreur.urls')),  # toutes les URLs de Livreur
    path('entreprise/', include("Entreprise.urls")),
]

# Pour que Django serve les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
