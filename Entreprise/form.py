

from django import forms
from .models import Entreprise
import re
from django.core.exceptions import ValidationError

class EntrepriseForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe sécurisé", "class": "form-control"}),
        label="Mot de passe"
    )
    mot_de_passe_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmez le mot de passe", "class": "form-control"}),
        label="Confirmation du mot de passe"
    )

    class Meta:
        model = Entreprise
        fields = ['nom', 'email', 'telephone', 'logo', 'description', 'mot_de_passe']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': "Nom de l'entreprise", 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': "Adresse email", 'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'placeholder': "Numéro de téléphone", 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': "Brève description de l'entreprise", 'rows': 4, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation = cleaned_data.get("mot_de_passe_confirmation")
        if mot_de_passe and confirmation and mot_de_passe != confirmation:
            self.add_error("mot_de_passe_confirmation", "Les mots de passe ne correspondent pas.")
        return cleaned_data

    # Nettoyage individuel des champs (nom, email, téléphone, mot de passe, description)
    def clean_nom(self):
        nom = self.cleaned_data.get('nom', '').strip()
        if len(nom) < 4:
            raise ValidationError("Le nom de l’entreprise doit comporter au moins 4 caractères.")
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\-_]+$', nom):
            raise ValidationError("Le nom contient des caractères non autorisés.")
        if Entreprise.objects.filter(nom__iexact=nom).exists():
            raise ValidationError("Ce nom d’entreprise existe déjà.")
        return nom

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("L’adresse email n’est pas valide.")
        if Entreprise.objects.filter(email__iexact=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone', '').strip()
        if not re.match(r'^(?:\+?\d{1,3})?[0-9]{8,15}$', telephone):
            raise ValidationError("Le numéro de téléphone doit contenir entre 8 et 15 chiffres.")
        if Entreprise.objects.filter(telephone=telephone).exists():
            raise ValidationError("Ce numéro de téléphone est déjà enregistré.")
        return telephone

    def clean_mot_de_passe(self):
        mot_de_passe = self.cleaned_data.get('mot_de_passe', '')
        if len(mot_de_passe) < 8:
            raise ValidationError("Le mot de passe doit comporter au moins 8 caractères.")
        if not re.search(r'[A-Z]', mot_de_passe):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
        if not re.search(r'[a-z]', mot_de_passe):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
        if not re.search(r'[0-9]', mot_de_passe):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[@$!%*#?&]', mot_de_passe):
            raise ValidationError("Le mot de passe doit contenir au moins un symbole spécial (@, $, !, %, *, #, ?, &).")
        return mot_de_passe

    def clean_description(self):
        desc = self.cleaned_data.get('description', '').strip()
        if len(desc) < 10:
            raise ValidationError("La description doit comporter au moins 10 caractères.")
        return re.sub(r'<[^>]*>', '', desc)  # Supprime tout code HTML (XSS)




    





        
#le formulaire login 
class EntrepriseLoginForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Entreprise
        fields = ['email', 'mot_de_passe']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mot_de_passe = cleaned_data.get('mot_de_passe')

        try:
            entreprise = Entreprise.objects.get(email=email)
        except Entreprise.DoesNotExist:
            raise forms.ValidationError("Aucune entreprise trouvée avec cet email.")

        if not entreprise.check_password(mot_de_passe):
            raise forms.ValidationError("Mot de passe incorrect.")

        if not entreprise.est_active:
            raise forms.ValidationError("Ce compte entreprise est désactivé.")

        cleaned_data['entreprise'] = entreprise
        return cleaned_data