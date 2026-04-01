# models.py

import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import timedelta



User = settings.AUTH_USER_MODEL 
# Récupération du modèle User central (Administrateur/User)
User = get_user_model()


# ==========================================================
# 🔹 LOCALISATION UNIVERSELLE
# ==========================================================
class Localisation(models.Model):
    """
    Localisation universelle pouvant être attachée à n'importe quel utilisateur
    (Client, Entreprise, Livreur, Partenaire, Correspondant, Administrateur).
    Utilise GenericForeignKey pour permettre la liaison à plusieurs modèles.
    """

    # ==========================================================
    # Référence générique vers n'importe quel modèle
    # ==========================================================
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    utilisateur = GenericForeignKey("content_type", "object_id")

    # ==========================================================
    # Champs de localisation
    # ==========================================================
    adresse = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Localisation"
        verbose_name_plural = "Localisations"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"Localisation de {self.utilisateur} - {self.ville}, {self.pays}"


# ==========================================================
# 🔹 CODE DE CRÉATION POUR LIVREUR / ENTREPRISE / PARTENAIRE
# ==========================================================
 # ou User si tu importes ton modèle personnalisé

# ==========================================================
# 🔹 CODE DE CRÉATION POUR LIVREUR / ENTREPRISE / PARTENAIRE / ADMIN
# ==========================================================
class Code_creation(models.Model):
    """
    Génère un code unique pour créer un utilisateur :
    livreur, partenaire, entreprise ou administrateur.
    Peut être créé par un super admin, un administrateur ou un partenaire.
    """

    # Référence au partenaire (facultative)
    partenaire = models.ForeignKey(
        'Partenaire.Partenaire',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="codes_crees"
    )

    # Référence à l'administrateur ou super admin (facultative)
    createur = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="codes_crees"
    )

    # Code unique (auto généré si non fourni)
    code = models.CharField(max_length=20, unique=True, editable=False)

    # Indique si le code a été utilisé
    utilise = models.BooleanField(default=False)

    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_utilisation = models.DateTimeField(null=True, blank=True)

    # Expiration automatique (2 jours après la création)
    expiration_code = models.DateTimeField(default=timezone.now() + timedelta(days=2))

    # Type de compte que ce code permet de créer
    TYPE_CHOICES = [
        ('livreur', 'Livreur'),
        ('entreprise', 'Entreprise'),
        ('partenaire', 'Partenaire'),
        ('administrateur', 'Administrateur'),  # nouveau type ajouté
    ]
    type_compte = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='livreur',
        help_text="Type de compte que ce code permettra de créer"
    )

    def save(self, *args, **kwargs):
        """
        Génération automatique du code si non fourni.
        Assure aussi que l'expiration est définie correctement.
        """
        if not self.code:
            self.code = self._generate_unique_code()

        # Définir l'expiration si non défini
        if not self.expiration_code:
            self.expiration_code = timezone.now() + timedelta(days=2)

        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        """
        Génère un code unique de 10 caractères en majuscules.
        """
        while True:
            code = uuid.uuid4().hex[:10].upper()
            if not Code_creation.objects.filter(code=code).exists():
                return code

    def __str__(self):
        user_or_partner = self.partenaire or self.createur
        return f"{self.code} - {user_or_partner} ({self.type_compte})"


# ==========================================================
# 🔹 PORTEFEUILLE CLIENT
# ==========================================================
class Portefeuille(models.Model):
    """
    Portefeuille pour gérer le solde et les transactions d'un utilisateur.
    Généralement attaché au client.
    """

    client = models.OneToOneField(
        User,  # Utilise le User central
        on_delete=models.CASCADE,
        related_name="portefeuille"
    )
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    devise = models.CharField(max_length=10, default="GNF")
    actif = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portefeuille de {self.client} - {self.solde} {self.devise}"


# ==========================================================
# 🔹 TRANSACTIONS DU PORTEFEUILLE
# ==========================================================
class TransactionPortefeuille(models.Model):
    """
    Historique des transactions liées au portefeuille.
    """

    TYPE_CHOICES = [
        ("credit", "Crédit"),
        ("debit", "Débit"),
        ("paiement", "Paiement"),
        ("remboursement", "Remboursement"),
    ]

    portefeuille = models.ForeignKey(
        Portefeuille,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_transaction} - {self.montant}"