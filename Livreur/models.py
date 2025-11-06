from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Livreur(models.Model):
    # Create your models here.
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom de famille du livreur."
    )

    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
        help_text="Prénom du livreur."
    )

    identifiant = models.CharField(
        max_length=20,
    validators=[MinLengthValidator(20)],
        unique=True,
        verbose_name="Identifiant",
        help_text="Identifiant unique utilisé pour l'identifié."
    )

    mail = models.EmailField(
        unique=True,
        verbose_name="Adresse e-mail",
        help_text="Adresse mail utilisée pour la connexion et la communication."
    )

    telephone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Téléphone",
        help_text="Numéro de Téléphone du livreur."
    )

    # -----------------------------------------------------------
    # 🧍 Informations supplémentaires
    # -----------------------------------------------------------

    profil = models.ImageField(
        upload_to='profils_livreur/',
        blank=True,
        null=True,
        verbose_name="Photo de profil",
        help_text="Image représentant le livreur (facultative)."
    )

    GENRE_CHOIX = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOIX,
        verbose_name="Genre",
        help_text="Sexe du livreur : M ou F."
    )

    date_naissance = models.DateField(
        verbose_name="Date de naissance",
        help_text="Date de naissance du livreur."
    )

    date_embauche = models.DateField(
        auto_now_add=False,
    verbose_name="Date de l'embauche",
    null=True,  
    blank=True  
    )

    actif = models.BooleanField(
        default=False,
        verbose_name="Statut de livreur"
    )

    vehicule = models.CharField(
        max_length=100,
        verbose_name="Voiture utilisé par le Livreur"
    )

    zone_livraison = models.CharField(
        max_length=100,
        verbose_name="Zone de livration"
    )

    # -----------------------------------------------------------
    # 🔑 Authentification et gestion
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
    # 🔎 Méthodes utiles
    # -----------------------------------------------------------

    def __str__(self):
        """
        Retourne une représentation lisible du livreur.
        Exemple : "Camara Fodé (fobic)"
        """
        return f"{self.nom} {self.prenom}"

    class Meta:
        verbose_name = "livreur"
        verbose_name_plural = "livreurs"
        ordering = ['-date_creation']
        db_table = "Livreur_livreur"
