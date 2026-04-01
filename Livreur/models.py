import uuid
import random
from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class Livreur(models.Model):
    """
    Profil spécifique pour le rôle Livreur.
    Toutes les informations sensibles (email, mot de passe, nom, prénom, téléphone...) sont dans User central.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_livreur"
    )

    # ============================================================
    # RELATIONS
    # ============================================================
    entreprise = models.ForeignKey(
        "Entreprise.Entreprise",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="livreurs",
        help_text="Entreprise à laquelle appartient le livreur"
    )

    partenaire = models.ForeignKey(
        "Partenaire.Partenaire",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="livreurs",
        help_text="Partenaire auquel appartient le livreur"
    )

    # Ajout du créateur du livreur
    createur = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="livreurs_crees",
    help_text="Utilisateur qui a créé ce livreur"
)

    code_livreur = models.OneToOneField(
        "Localisation.Code_creation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="livreur",
        help_text="Code unique de création du livreur"
    )

    # ============================================================
    # VERIFICATION / SECURITE
    # ============================================================
    confirmation_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="UUID pour le lien sécurisé de confirmation"
    )
    code_verification = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="Code numérique de 6 chiffres pour vérification par email ou SMS"
    )
    compte_confirme = models.BooleanField(default=False)
    token_expiration = models.DateTimeField(null=True, blank=True)

    def generer_token(self):
        """
        Génère un token UUID et un code de 6 chiffres pour vérification.
        Définit aussi l'expiration dans 1 heure.
        """
        self.confirmation_token = uuid.uuid4()
        self.code_verification = f"{random.randint(100000, 999999):06}"
        self.token_expiration = timezone.now() + timedelta(hours=1)
        self.compte_confirme = False
        self.save()

    # ============================================================
    # INFORMATIONS SPECIFIQUES
    # ============================================================
    vehicule = models.CharField(max_length=100, null=True, blank=True)
    zone_livraison = models.CharField(max_length=150, null=True, blank=True)

    # ============================================================
    # STATUT
    # ============================================================
    STATUT_CHOIX = (
        ('en_attente', 'En attente'),
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOIX,
        default='en_attente',
        db_index=True
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    # ============================================================
    # VALIDATION METIER
    # ============================================================
    def clean(self):
        """
        Vérifie que le livreur appartient à UNE seule entité.
        """
        super().clean()
        if self.entreprise and self.partenaire:
            raise ValidationError("Un livreur ne peut pas appartenir à une entreprise ET un partenaire.")
        if not self.entreprise and not self.partenaire:
            raise ValidationError("Le livreur doit être lié à une entreprise OU un partenaire.")

    def __str__(self):
        # Affiche le nom complet si présent, sinon l'email
        return f"{self.user.nom} {self.user.prenom}" if self.user.nom and self.user.prenom else self.user.email

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Livreur"
        verbose_name_plural = "Livreurs"