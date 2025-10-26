from django.contrib import admin

from .models import Livreur

@admin.register(Livreur)
class LivreurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'date_embauche', 'actif', 'vehicule', 'zone_livraison')
    list_filter = ('actif', 'sexe', 'zone_livraison')
    search_fields = ('nom', 'prenom', 'email', 'telephone', 'matricule')
    ordering = ('nom', 'prenom')
    date_hierarchy = 'date_embauche'
    readonly_fields = ('date_embauche',)
# Register your models here.

