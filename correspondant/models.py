# Shopi/Correspondant/models.py

from django.db import models
from django.conf import settings  # Pour utiliser le User personnalisé
from django.utils import timezone

# ==========================================================
# 🔹 Modèle Correspondant
# ==========================================================
class Correspondant(models.Model):
    """
    Modèle pour gérer les correspondants de la plateforme.
    Chaque correspondant est lié à un User avec le rôle 'correspondant'.
    """

    # Relation vers le User central
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="correspondant_profile"
    )

    # Informations personnelles supplémentaires (facultatives)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)

    # Statut du correspondant
    actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    # Champs spécifiques
    description = models.TextField(blank=True, null=True)
    photo_profil = models.ImageField(upload_to='correspondants/', blank=True, null=True)

    class Meta:
        verbose_name = "Correspondant"
        verbose_name_plural = "Correspondants"

    def __str__(self):
        return f"{self.user.nom_complet()} ({self.user.email})"