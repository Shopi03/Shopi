from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client
from .forms import ClientInscriptionForm, ClientLoginForm, ClientModificationForm

# --- INSCRIPTION ---
def inscription_client(request):
    if request.method == "POST":
        form = ClientInscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie ! Connectez-vous maintenant.")
            return redirect('login_client')
    else:
        form = ClientInscriptionForm()
    return render(request, 'client/inscription_client.html', {'form': form})


# --- CONNEXION ---
def login_client(request):
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                client = Client.objects.get(email=email)
                if client.check_password(password):
                    request.session['client_id'] = client.id
                    messages.success(request, f"Bienvenue {client.nom} !")
                    return redirect('liste_clients')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Client.DoesNotExist:
                messages.error(request, "Aucun compte trouvé avec cet e-mail.")
    else:
        form = ClientLoginForm()
    return render(request, 'client/login_client.html', {'form': form})


# --- LISTE DES CLIENTS ---
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'client/liste_clients.html', {'clients': clients})


# --- MODIFICATION ---
def modifier_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = ClientModificationForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil modifié avec succès.")
            return redirect('liste_clients')
    else:
        form = ClientModificationForm(instance=client)
    return render(request, 'client/modifier_client.html', {'form': form, 'client': client})


# --- SUPPRESSION ---
def supprimer_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Client supprimé avec succès.")
        return redirect('liste_clients')
    return render(request, 'client/supprimer_client.html', {'client': client})
