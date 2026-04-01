from django.db import models
from django.conf import settings

class Partenaire(models.Model):
    """
    Profil spécifique pour le rôle Partenaire.
    Toutes les informations sensibles sont dans User central.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_partenaire"
    )
    
    pseudo = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='partenaires/', blank=True, null=True)
    entreprise = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}" if self.user.nom else f"{self.user.email}"

    def full_name(self):
        return f"{self.user.nom} {self.user.prenom}" if self.user.nom else self.user.email

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['-user__date_joined']