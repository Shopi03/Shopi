from django import forms
from .models import Client
from django.contrib.auth.hashers import make_password

class ClientInscriptionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'telephone', 'date_naissance', 'sexe', 'profil', 'password']
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "date_naissance": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "sexe": forms.Select(attrs={"class": "form-control"}),
            "profil": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "confirmation": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('confirmation')

        if password and confirmation and password != confirmation:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        client = super().save(commit=False)
        client.password = make_password(self.cleaned_data['password'])
        if commit:
            client.save()
        return client


class ClientLoginForm(forms.Form):
    email = forms.EmailField(label="Adresse e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


class ClientModificationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'telephone', 'date_naissance', 'sexe', 'profil', 'actif']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
