from django import forms
from .models import Entreprise, Produit, Commande
class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ["nom", "email", "telephone", "logo", "description"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        labels = {
            "nom": "Nom de l'entreprise",
            "email": "Adresse e-mail",
            "telephone": "Numéro de téléphone",
            "logo": "Logo de l'entreprise",
            "description": "Description de l'entreprise",
        }
        error_messages = {
            "nom": {
                "max_length": "Le nom de l'entreprise ne peut pas dépasser 200 caractères.",
                "required": "Le nom de l'entreprise est obligatoire.",
            },  
            "email": {
                "invalid": "Entrez une adresse e-mail valide.",
                "required": "L'adresse e-mail est obligatoire.",
            },
            "telephone": {
                "max_length": "Le numéro de téléphone ne peut pas dépasser 15 caractères.",
                "required": "Le numéro de téléphone est obligatoire.",
            },
            "description": {
                "required": "La description de l'entreprise est obligatoire.",
            },
        }
        
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ["entreprise", "nom", "description", "prix", "stock", "image", "categorie", "sous_categorie", "marque", "couleur", "taille", "poids", "disponibilite"]
        widgets = {
            "entreprise": forms.Select(attrs={"class": "form-control"}),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "prix": forms.NumberInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "categorie": forms.TextInput(attrs={"class": "form-control"}),
            "sous_categorie": forms.TextInput(attrs={"class": "form-control"}),
            "marque": forms.TextInput(attrs={"class": "form-control"}),
            "couleur": forms.TextInput(attrs={"class": "form-control"}),
            "taille": forms.TextInput(attrs={"class": "form-control"}),
            "poids": forms.NumberInput(attrs={"class": "form-control"}),
            "disponibilite": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "entreprise": "Entreprise",
            "nom": "Nom du produit",
            "description": "Description du produit",
            "prix": "Prix",
            "stock": "Stock disponible",
            "image": "Image du produit",
            "categorie": "Catégorie",
            "sous_categorie": "Sous-catégorie",
            "marque": "Marque",
            "couleur": "Couleur",
            "taille": "Taille",
            "poids": "Poids",
            "disponibilite": "Disponible",
        }
        error_messages = {
            "nom": {
                "max_length": "Le nom du produit ne peut pas dépasser 200 caractères.",
                "required": "Le nom du produit est obligatoire.",
            },
            "description": {
                "required": "La description du produit est obligatoire.",
            },
            "prix": {
                "invalid": "Entrez un prix valide.",
                "required": "Le prix est obligatoire.",
            },
            "stock": {
                "invalid": "Entrez un stock valide.",
                "required": "Le stock est obligatoire.",
            },
            "categorie": {
                "max_length": "La catégorie ne peut pas dépasser 100 caractères.",
                "required": "La catégorie est obligatoire.",
            },
            "sous_categorie": {
                "max_length": "La sous-catégorie ne peut pas dépasser 100 caractères.",
                "required": "La sous-catégorie est obligatoire.",
            },
            "marque": {
                "max_length": "La marque ne peut pas dépasser 100 caractères.",
                "required": "La marque est obligatoire.",
            },
            "couleur": {
                "max_length": "La couleur ne peut pas dépasser 50 caractères.",
                "required": "La couleur est obligatoire.",
            },
            "taille": {
                "max_length": "La taille ne peut pas dépasser 20 caractères.",
                "required": "La taille est obligatoire.",
            },
            "poids": {
                "invalid": "Entrez un poids valide.",
                "required": "Le poids est obligatoire.",
            },
            
        }
        
        