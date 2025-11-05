from django.shortcuts import redirect
from django.contrib import messages

def livreur_login_required(view_func):
    """
    Décorateur pour protéger les vues.
    Empêche l'accès aux utilisateurs non connectés.
    """
    def wrapper(request, *args, **kwargs):
        if 'livreur_id' not in request.session:
            messages.warning(request, "Veuillez vous connecter pour accéder à cette page.")
            return redirect('login_livreur')
        return view_func(request, *args, **kwargs)
    return wrapper