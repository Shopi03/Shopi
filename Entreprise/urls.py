
from django.contrib import admin
from django.urls import path


from .views import *
from . import views


urlpatterns = [
# les chemin des entreprises ajouter dans le systeme
    path("tableau_de_bord/",views.tableau_bord, name="tableau_de_bord"),
    path("home/",views.home, name="home"),
    path("inscription_entreprise/",views.inscription_entreprise, name="inscription_entreprise"),
    path("modification_entreprise/<int:id>/",views.modification_entreprise, name="modification_entreprise"),
    path('liste_entreprise/', views.liste_entreprise, name='liste_entreprise'),
        path('suppression_entreprise/<int:id>/', views.suppression_entreprise, name='suppression_entreprise'),



    #les chemin des produits ajouté
    


]

