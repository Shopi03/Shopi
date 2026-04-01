from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# ============================================================
# ABONNEMENT (FOLLOW ENTRE TOUS LES TYPES D’UTILISATEURS)
# ============================================================

class Abonnement(models.Model):
    """
    Permet à n'importe quel type d'utilisateur de suivre un autre
    (client, entreprise, livreur, partenaire, etc.).
    Utilise GenericForeignKey pour supporter plusieurs modèles.
    """

    # ---------- QUI S'ABONNE ----------
    # Type du modèle (Client, Entreprise, etc.)
    abonne_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="abonnements_effectues"
    )

    # ID de l'objet abonné
    abonne_object_id = models.PositiveIntegerField()

    # Référence générique vers l'objet abonné
    abonne = GenericForeignKey(
        "abonne_content_type",
        "abonne_object_id"
    )

    # ---------- QUI EST SUIVI ----------
    cible_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="abonnements_recus"
    )
    cible_object_id = models.PositiveIntegerField()
    cible = GenericForeignKey(
        "cible_content_type",
        "cible_object_id"
    )

    # Abonnement actif ou non
    actif = models.BooleanField(default=True)

    # Date de création
    date_abonnement = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Empêche le double abonnement
        unique_together = (
            "abonne_content_type",
            "abonne_object_id",
            "cible_content_type",
            "cible_object_id",
        )

    def __str__(self):
        return f"{self.abonne} suit {self.cible}"


# ============================================================
# CONVERSATION (FIL DE DISCUSSION)
# ============================================================

class Conversation(models.Model):
    """
    Représente une discussion (privée ou groupe).
    Les participants sont stockés dans ParticipantConversation.
    """

    # Date de création de la conversation
    cree_le = models.DateTimeField(auto_now_add=True)

    # Permet d’archiver/désactiver une conversation
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"Conversation {self.id}"


# ============================================================
# PARTICIPANTS À UNE CONVERSATION
# ============================================================

class ParticipantConversation(models.Model):
    """
    Liste des utilisateurs présents dans une conversation.
    Supporte tous les types d’utilisateurs grâce à GenericForeignKey.
    """

    # Conversation concernée
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="participants"
    )

    # Type du modèle utilisateur
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    # ID de l’utilisateur
    object_id = models.PositiveIntegerField()

    # Référence générique vers l’utilisateur
    utilisateur = GenericForeignKey("content_type", "object_id")

    # Date d’ajout dans la conversation
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Empêche d’ajouter deux fois le même utilisateur
        unique_together = ("conversation", "content_type", "object_id")

    def __str__(self):
        return f"{self.utilisateur} dans conversation {self.conversation.id}"


# ============================================================
# MESSAGE (COEUR DU CHAT)
# ============================================================

class Message(models.Model):
    """
    Message envoyé dans une conversation.
    Compatible avec tous les types d’expéditeurs.
    """

    # Conversation liée
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    # ---------- EXPÉDITEUR ----------
    expediteur_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    expediteur_object_id = models.PositiveIntegerField()

    # Référence générique vers l’expéditeur
    expediteur = GenericForeignKey(
        "expediteur_content_type",
        "expediteur_object_id"
    )

    # Contenu texte du message
    contenu = models.TextField(blank=True, null=True)

    # Fichier joint (image, pdf, etc.)
    fichier = models.FileField(
        upload_to="messages/",
        null=True,
        blank=True
    )

    # Indique si le message a été lu
    lu = models.BooleanField(default=False)

    # Date d’envoi
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id}"