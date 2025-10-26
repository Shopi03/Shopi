from django.db import models

class Livreur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=20)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    date_embauche = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    password = models.CharField(max_length=128)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('homme', 'Homme'), ('femme', 'Femme')])
    profil = models.ImageField(upload_to='livreurs_profiles/', null=True, blank=True)
    vehicule = models.CharField(max_length=100)
    zone_livraison = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    class Meta:
        verbose_name = "Livreur"
        verbose_name_plural = "Livreurs"
# Create your models here.
