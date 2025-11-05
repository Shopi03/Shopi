from django.contrib import admin

from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'date_inscription', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    ordering = ('nom', 'prenom')
    date_hierarchy = 'date_inscription'
    readonly_fields = ('date_inscription',)
