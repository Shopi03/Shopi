from django.db import models

"""
Modèle représentant un Partenaire dans la plateforme SHOPI.
Chaque partenaire possède ses informations personnelles et un compte d'accès.
"""

# -----------------------------------------------------------
#  Identité du partenaire
# -----------------------------------------------------------

# L'identifiant unique est créé automatiquement par Django (champ "id" implicite)
class Partenaire(models.Model):

    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom de famille du partenaire."
    )

    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
        help_text="Prénom du partenaire."
    )

    pseudo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom d'utilisateur (pseudo)",
        help_text="Nom unique utilisé pour se connecter."
    )

    mail = models.EmailField(
        unique=True,
        verbose_name="Adresse e-mail",
        help_text="Adresse mail utilisée pour la connexion et la communication."
    )

    # -----------------------------------------------------------
    #  Informations supplémentaires
    # -----------------------------------------------------------

    profil = models.ImageField(
        upload_to='profils_partenaire/',
        blank=True,
        null=True,
        verbose_name="Photo de profil",
        help_text="Image représentant le partenaire (facultative)."
    )

    GENRE_CHOIX = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOIX,
        verbose_name="Genre",
        help_text="Sexe du partenaire : M ou F."
    )

    date_naissance = models.DateField(
        verbose_name="Date de naissance",
        help_text="Date de naissance du partenaire."
    )

    # -----------------------------------------------------------
    #  Authentification et gestion
    # -----------------------------------------------------------

    mot_de_passe = models.CharField(
        max_length=255,
        verbose_name="Mot de passe",
        help_text="Mot de passe chiffré pour l'accès au compte."
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création du compte"
    )

    # -----------------------------------------------------------
    #  Méthodes utiles
    # -----------------------------------------------------------

    def __str__(self):
        """
        Retourne une représentation lisible du partenaire.
        Exemple : "Camara Fodé (fobic)"
        """
        return f"{self.nom} {self.prenom} ({self.pseudo})"

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['-date_creation']