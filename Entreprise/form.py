from django import forms
from .models import Entreprise, Produit, Commande
from django.contrib.auth.hashers import make_password

class EntrepriseForm(forms.ModelForm):
    # Champs supplémentaires pour le mot de passe et confirmation
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    confirmation = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Entreprise
        fields = ["nom", "email", "telephone", "logo", "description", "mot_de_passe", "actif"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "mot_de_passe": forms.PasswordInput(attrs={"class": "form-control"}),
            "actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nom": "Nom de l'entreprise",
            "email": "Adresse e-mail",
            "telephone": "Numéro de téléphone",
            "logo": "Logo de l'entreprise",
            "description": "Description de l'entreprise",
            "mot_de_passe": "Mot de passe",
            "actif": "Actif",
        }
        error_messages = {
            "nom": {"max_length": "Le nom de l'entreprise ne peut pas dépasser 200 caractères.", "required": "Le nom de l'entreprise est obligatoire."},
            "email": {"invalid": "Entrez une adresse e-mail valide.", "required": "L'adresse e-mail est obligatoire."},
            "telephone": {"max_length": "Le numéro de téléphone ne peut pas dépasser 15 caractères.", "required": "Le numéro de téléphone est obligatoire."},
            "description": {"required": "La description de l'entreprise est obligatoire."},
            "mot_de_passe": {"required": "Le mot de passe est obligatoire."},
            "confirmation": {"required": "La confirmation du mot de passe est obligatoire."},
        }

    # Vérification doublon email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Entreprise.objects.filter(email=email).exists():
            raise forms.ValidationError("Une entreprise avec cet email existe déjà.")
        return email

    # Vérification correspondance mot de passe
    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('mot_de_passe')
        confirmation = cleaned_data.get('confirmation')

        if mot_de_passe and confirmation:
            if mot_de_passe != confirmation:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data
    
    # la validation du numero de telephone
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not telephone.isdigit():
            raise forms.ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")
        if len(telephone) < 8:
            raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
        return telephone
    
    
    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('mot_de_passe')
        confirmation = cleaned_data.get('confirmation')
        if mot_de_passe and confirmation and mot_de_passe != confirmation:
            self.add_error('confirmation', "Les mots de passe ne correspondent pas.")
        elif mot_de_passe and len(mot_de_passe) < 6:
            self.add_error('mot_de_passe', "Le mot de passe doit contenir au moins 6 caractères.")
        return cleaned_data


    # Sauvegarde avec hachage du mot de passe
    def save(self, commit=True):
        entreprise = super().save(commit=False)
        entreprise.mot_de_passe = make_password(self.cleaned_data["mot_de_passe"])
        if commit:
            entreprise.save()
        return entreprise




    





        
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