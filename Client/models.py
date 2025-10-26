from django.db import models



class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    date_inscription = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    password = models.CharField(max_length=128)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('homme', 'Homme'), ('femme', 'Femme')])
    profil = models.ImageField(upload_to='profiles/', null=True, blank=True)
    def __str__(self):
        return f" {self.nom} {self.prenom}"
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
