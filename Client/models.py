from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    date_inscription = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    password = models.CharField(max_length=128)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('homme', 'Homme'), ('femme', 'Femme')])
    profil = models.ImageField(upload_to='media/client_profiles/', null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
