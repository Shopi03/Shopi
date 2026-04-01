# fichier : livreur/views.py

import random
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from Livreur.models import Livreur
from Administrateur.models import User
# -------------------------------------------------------------------
# TABLEAU DE BORD LIVREUR
# -------------------------------------------------------------------



def tableau_de_bord_livreur(request):


    if getattr(request.user, "role", "").lower() != "livreur":
        return redirect("login")  # rediriger si pas partenaire

    livreur = request.user

    context = {
        "livreur":livreur
    }

    return render(request, 'livreur/tableau_de_bord.livreur.html', 
        context
    )




# -------------------------------------------------------------------
# VERIFICATION CODE CREATION COMPTE LIVREUR
# ------------------------------------------------------------------

