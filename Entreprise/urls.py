
from django.contrib import admin
from django.urls import path


from .views import *
from . import views


urlpatterns = [
# les chemin des entreprises ajouter dans le systeme
    path("tableau_de_bord/",views.tableau_bord, name="tableau_de_bord"),
    path("home/",views.home, name="home"),
    path("creer_entreprise/",views.creer_entreprise, name="creer_entreprise"),

  



    #les chemin des produits ajouté
    


]

