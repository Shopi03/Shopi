from django.db import models
from django.conf import settings

class Client(models.Model):
    """
    Profil spécifique pour le rôle Client.
    Toutes les informations sensibles (email, mot de passe, nom, prénom, téléphone...) sont dans User central.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Lien vers le User central
        on_delete=models.CASCADE,
        related_name="profil_client"
    )

    # Champs spécifiques au Client (exemple)
    numero_client = models.CharField(max_length=50, blank=True, null=True)
    points_fidelite = models.IntegerField(default=0)

    def __str__(self):
        # Affiche le nom complet si présent, sinon l'email
        return f"{self.user.nom} {self.user.prenom}" if self.user.nom and self.user.prenom else self.user.email

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"