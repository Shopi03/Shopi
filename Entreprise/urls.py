
from django.contrib import admin
from django.urls import path


from .views import *
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("ajout_entreprise/",views.ajout_entreprise, name="ajout_entreprise"),
    path("modification_entreprise/<int:id>/",views.modification_entreprise, name="modification_entreprise"),
    path("liste_entreprise/",views.home, name="liste_entreprise"),
    path("ajout_produit/",views.ajout_produit, name="ajout_produit"),
    path("modification_produit/<int:id>/",views.modification_produit, name="modification_produit"),

]

