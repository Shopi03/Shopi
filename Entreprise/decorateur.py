# decorators.py
from django.shortcuts import redirect

def entreprise_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'entreprise_id' not in request.session:
            return redirect('entreprise_login')
        return view_func(request, *args, **kwargs)
    return wrapper
