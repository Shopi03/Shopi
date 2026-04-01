# Administrateur/views/views_code_creation.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CodeCreation, User, Partenaire

# Decorateur combiné : super admin, admin ou partenaire
def code_creation_access(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté.")
            return redirect("login")
        role = getattr(request.user, "role", "")
        if role not in ["super_admin", "administrateur", "partenaire"]:
            messages.error(request, "Accès refusé.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@code_creation_access
def gestion_code_creation(request):
    """
    Permet à un super admin, admin ou partenaire de générer des codes.
    """
    if request.method == "POST":
        type_compte = request.POST.get("type_compte")
        partenaire_id = request.POST.get("partenaire")  # facultatif
        partenaire = Partenaire.objects.filter(id=partenaire_id).first() if partenaire_id else None

        code = CodeCreation.objects.create(
            type_compte=type_compte,
            createur=request.user,
            partenaire=partenaire
        )
        messages.success(request, f"Code généré : {code.code} pour {type_compte}")

    # Liste des codes générés par cet utilisateur ou si super_admin voit tous
    role = getattr(request.user, "role", "")
    if role == "super_admin":
        codes = CodeCreation.objects.all().order_by("-date_creation")
    else:
        codes = CodeCreation.objects.filter(createur=request.user).order_by("-date_creation")

    # Partenaires disponibles pour sélection si le user est admin ou super_admin
    partenaires = Partenaire.objects.all() if role in ["super_admin", "administrateur"] else None

    context = {
        "codes": codes,
        "partenaires": partenaires
    }

    return render(request, "administrateur/code_creation/gestion_code_creation.html", context)