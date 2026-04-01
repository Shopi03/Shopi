# Administrateur/admin.py

from django.contrib import admin
from .models import Code_creation


@admin.register(Code_creation)
class CodeCreationAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage du modèle Code_creation
    dans l'interface d'administration Django.
    """

    # Colonnes visibles dans la liste
    list_display = (
        'code',
        'type_compte',
        'partenaire',
        'createur',
        'utilise',
        'date_creation',
        'date_utilisation'
    )

    # Filtres dans la barre latérale droite
    list_filter = (
        'type_compte',
        'utilise',
        'date_creation'
    )

    # Champ de recherche
    search_fields = (
        'code',
        'partenaire__nom',
        'createur__email'
    )

    # Tri par défaut
    ordering = ('-date_creation',)

    # Champs non modifiables dans l'admin
    readonly_fields = (
        'code',
        'date_creation',
        'date_utilisation'
    )

    # Organisation du formulaire dans l'admin
    fieldsets = (
        ("Informations du code", {
            'fields': ('code', 'type_compte', 'utilise')
        }),

        ("Créateur du code", {
            'fields': ('partenaire', 'createur')
        }),

        ("Dates", {
            'fields': ('date_creation', 'date_utilisation')
        }),
    )