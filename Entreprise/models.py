from django.db import models
from Livreur.models import Livreur
from Client.models import Client
from Partenaire.models import Partenaire
from django.conf import settings
from django.utils.text import slugify




# ==========================================================
# PROFIL ENTREPRISE
# ==========================================================
class Entreprise(models.Model):
    """
    Profil spécifique pour le rôle Entreprise.
    Toutes les informations générales sont dans le modèle User.
    Ce modèle stocke uniquement les informations propres à une entreprise.
    """

    # Lien direct avec l'utilisateur (rôle 'entreprise')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_entreprise",
        verbose_name="Utilisateur associé"
    )

    # ------------------------------------------------------
    # Informations publiques de l'entreprise
    # ------------------------------------------------------
    designation = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Nom de l'entreprise",
        help_text="Nom officiel de l'entreprise"
    )
    logo = models.ImageField(
        upload_to="entreprises/logos/",
        blank=True,
        null=True,
        verbose_name="Logo de l'entreprise"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Présentation de l'entreprise"
    )
    savoir_faire = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Savoir-faire",
        help_text="Compétences ou services offerts par l'entreprise"
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site Web",
        help_text="URL du site officiel"
    )

    # ------------------------------------------------------
    # Statut
    # ------------------------------------------------------
    actif = models.BooleanField(
        default=True,
        verbose_name="Entreprise active",
        help_text="Si l'entreprise est active ou désactivée"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création du profil"
    )
    date_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière mise à jour"
    )

    # ------------------------------------------------------
    # Méthodes
    # ------------------------------------------------------
    def __str__(self):
        return self.designation or self.user.nom_complet() or self.user.email

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ["-date_creation"]


class Produit(models.Model):
    STATUS_CHOICES = [
        ('Published', 'Published'),
        ('Scheduled', 'Scheduled'),
        ('Draft', 'Draft'),
    ]
    VISIBILITY_CHOICES = [
        ('Public', 'Public'),
        ('Hidden', 'Hidden'),
    ]

    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_principale = models.ImageField(upload_to='produits/', blank=True, null=True)
    fabricant = models.CharField(max_length=255, blank=True, null=True)
    marque = models.CharField(max_length=255, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    commandes = models.PositiveIntegerField(default=0)
    statut = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Published')
    visibilite = models.CharField(max_length=50, choices=VISIBILITY_CHOICES, default='Public')
    categorie = models.CharField(max_length=100, blank=True, null=True)
    meta_titre = models.CharField(max_length=255, blank=True, null=True)
    meta_mots_cles = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    date_publication = models.DateTimeField(blank=True, null=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Commande(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_commande = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    adresse_livraison = models.CharField(max_length=200)


class Validation(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    partenaire = models.ForeignKey(Partenaire, related_name='partenaires', on_delete=models.CASCADE, null=True, blank=True)
    date_validation = models.DateField(auto_now_add=True)
    code_validation_entreprise = models.CharField(max_length=10)
    code_validation_client = models.CharField(max_length=10)
    code_validation_livreur = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Commande {self.id} - {self.entreprise.nom}"

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"