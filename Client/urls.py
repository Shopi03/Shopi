from django.urls import path
from . import views

urlpatterns = [
    path('inscription_client/', views.inscription_client, name='inscription_client'),
    path('login_client/', views.login_client, name='login_client'),
    path('liste_clients/', views.liste_clients, name='liste_clients'),
    path('modifier_client/<int:client_id>/', views.modifier_client, name='modifier_client'),
    path('supprimer_client/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
]
