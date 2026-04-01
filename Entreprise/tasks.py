# Entreprise/tasks.py
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shopi.settings")
django.setup()

from Localisation.models import Code_creation
from django.contrib.auth import get_user_model

User = get_user_model()

def supprimer_comptes_expirés():
    limite = timezone.now() - timedelta(hours=48)
    codes_expire = Code_creation.objects.filter(
        type_compte="entreprise",
        utilise=True,
        date_creation__lt=limite
    )

    for code in codes_expire:
        user = User.objects.filter(code_creation=code).first()
        if user:
            user.delete()
        code.utilise = False
        code.save()

if __name__ == "__main__":
    supprimer_comptes_expirés()