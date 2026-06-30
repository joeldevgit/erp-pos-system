from django.shortcuts import redirect
from django.contrib import messages


def grupos_requeridos(*nombres_grupos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.groups.filter(name__in=nombres_grupos).exists():
                return view_func(request, *args, **kwargs)

            messages.error(request, "No tienes permiso para acceder a esta sección.")
            return redirect("/")
        return wrapper
    return decorator