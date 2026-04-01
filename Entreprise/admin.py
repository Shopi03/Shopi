from django.contrib import admin
from .models import Entreprise, Produit, Commande


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    # Utiliser des fonctions pour afficher les champs liés à User
    list_display = ('get_nom', 'get_email', 'get_telephone', 'date_creation', 'actif', 'logo')
    list_filter = ('actif', 'date_creation')
    search_fields = ('user__nom', 'user__email', 'user__telephone')
    ordering = ('-date_creation',)
    readonly_fields = ('date_creation',)

    # Fonctions pour afficher les champs du user
    def get_nom(self, obj):
        return obj.user.nom
    get_nom.short_description = "Nom"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

    def get_telephone(self, obj):
        return obj.user.telephone
    get_telephone.short_description = "Téléphone"


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'titre', 'prix', 'stock', 'statut', 'visibilite', 'date_publication', 'cree_le', 'image_principale')
    list_filter = ('entreprise', 'statut', 'visibilite', 'date_publication')
    search_fields = ('entreprise__user__nom', 'titre')
    ordering = ('-date_publication',)
    readonly_fields = ('cree_le',)