from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import uuid


# ==========================================================
# MANAGER PERSONNALISÉ
# ==========================================================
class UserManager(BaseUserManager):

    # Création utilisateur normal
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    # Création super administrateur
    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "super_admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superuser doit avoir is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superuser doit avoir is_superuser=True")

        return self.create_user(email, password, **extra_fields)



# ==========================================================
# MODELE UTILISATEUR PERSONNALISÉ
# ==========================================================
class User(AbstractBaseUser, PermissionsMixin):

    # ------------------------------------------------------
    # Identifiant public sécurisé
    # ------------------------------------------------------
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    # ------------------------------------------------------
    # Rôles utilisateurs
    # ------------------------------------------------------
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('livreur', 'Livreur'),
        ('entreprise', 'Entreprise'),
        ('partenaire', 'Partenaire'),
        ('admin', 'Administrateur'),
        ('super_admin', 'Super Administrateur'),
        ('correspondant', 'Correspondant'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client',
        db_index=True
    )


    # ------------------------------------------------------
    # Relation avec Code_creation
    # ------------------------------------------------------
    code_creation = models.ForeignKey(
        "Localisation.Code_creation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="utilisateurs"
    )


    # ------------------------------------------------------
    # Informations principales
    # ------------------------------------------------------
    email = models.EmailField(
        unique=True,
        db_index=True
    )

    nom = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    prenom = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    telephone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_index=True
    )


    # ------------------------------------------------------
    # Localisation
    # ------------------------------------------------------
    pays = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    ville = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    adresse = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    # Coordonnées GPS (pour géolocalisation)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )


    # ------------------------------------------------------
    # Profil utilisateur
    # ------------------------------------------------------
    profil = models.ImageField(
        upload_to='users/profils/',
        blank=True,
        null=True
    )

    date_naissance = models.DateField(
        blank=True,
        null=True
    )

    sexe = models.CharField(
        max_length=10,
        choices=[
            ('homme', 'Homme'),
            ('femme', 'Femme')
        ],
        blank=True,
        null=True
    )


    # ------------------------------------------------------
    # Vérification du compte
    # ------------------------------------------------------
    email_verifie = models.BooleanField(default=False)

    telephone_verifie = models.BooleanField(default=False)

    code_verification = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    code_expiration = models.DateTimeField(
        blank=True,
        null=True
    )


    # ------------------------------------------------------
    # Statut du compte
    # ------------------------------------------------------
    STATUT_CHOICES = (
        ("actif", "Actif"),
        ("suspendu", "Suspendu"),
        ("en_attente", "En attente"),
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="en_attente"
    )

    raison_suspension = models.TextField(
        blank=True,
        null=True
    )


    # ------------------------------------------------------
    # Réputation (avis clients)
    # ------------------------------------------------------
    note = models.FloatField(default=0)

    nombre_avis = models.IntegerField(default=0)


    # ------------------------------------------------------
    # Activité utilisateur
    # ------------------------------------------------------
    last_seen = models.DateTimeField(
        blank=True,
        null=True
    )

    est_en_ligne = models.BooleanField(default=False)


    # ------------------------------------------------------
    # Permissions Django
    # ------------------------------------------------------
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(
        default=False,
        help_text="Accès à l'administration Django"
    )


    # ------------------------------------------------------
    # Dates importantes
    # ------------------------------------------------------
    date_joined = models.DateTimeField(auto_now_add=True)

    date_update = models.DateTimeField(auto_now=True)


    # ------------------------------------------------------
    # Manager
    # ------------------------------------------------------
    objects = UserManager()


    # ------------------------------------------------------
    # Authentification
    # ------------------------------------------------------
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []


    # ------------------------------------------------------
    # Nom complet utilisateur
    # ------------------------------------------------------
    def nom_complet(self):

        return f"{self.prenom or ''} {self.nom or ''}".strip() or self.email


    def __str__(self):
        return self.nom_complet()


    # ------------------------------------------------------
    # Meta configuration
    # ------------------------------------------------------
    class Meta:

        ordering = ["-date_joined"]

        verbose_name = "Utilisateur"

        verbose_name_plural = "Utilisateurs"