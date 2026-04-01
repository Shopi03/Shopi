# SHOPI/urls.py

from django.contrib import admin
from django.urls import path, include

# Pour servir les fichiers médias et statiques en développement
from django.conf import settings
from django.conf.urls.static import static

from Administrateur.view import views

urlpatterns = [

    # ---------------- ADMIN DJANGO ----------------
    path('admin/', admin.site.urls),

    # ---------------- LOGIN MULTI-RÔLE ----------------
    path('login/', views.login_multi, name='login'),

    # ---------------- MOT DE PASSE OUBLIÉ / RÉINITIALISATION ----------------
    path('mot_de_passe_oubliez/', views.mot_de_passe_oubliez, name='mot_de_passe_oubliez'),
    path('verification_code/', views.verification_code, name='verification_code'),
    path('nouveau_mot_de_passe/', views.nouveau_mot_de_passe, name='nouveau_mot_de_passe'),
    path('mot_de_passe_reinitialiser/', views.mot_de_passe_reinitialiser, name='mot_de_passe_reinitialiser'),

    # ---------------- APPS ----------------
    path('partenaire/', include('Partenaire.urls')),
    path('livreur/', include('Livreur.urls')),
    path('entreprise/', include('Entreprise.urls')),
    path('client/', include('Client.urls')),
    path('administrateur/', include('Administrateur.urls')),
    path('localisation/', include('Localisation.urls')),

]

# ---------------- MEDIA & STATIC ----------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)