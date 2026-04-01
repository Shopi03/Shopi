
from django.urls import path
from Livreur.view import views

urlpatterns = [
    # Afficher tous les livreurs
    path('tableau_de_bord_livreur/', views.tableau_de_bord_livreur, name='tableau_de_bord_livreur'),
    
  
  
   

  
]