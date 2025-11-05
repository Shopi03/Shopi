
from django.contrib import admin
from django.urls import path


from .views import *
from . import views


urlpatterns = [
# les chemin des entreprises ajouter dans le systeme
    path("inscription_entreprise/",views.inscription_entreprise, name="inscription_entreprise"),
    path("modification_entreprise/<int:id>/",views.modification_entreprise, name="modification_entreprise"),
    path('liste_entreprise/', views.liste_entreprise, name='liste_entreprise'),
        path('suppression_entreprise/<int:id>/', views.suppression_entreprise, name='suppression_entreprise'),



    #les chemin des produits ajouté
    


]

