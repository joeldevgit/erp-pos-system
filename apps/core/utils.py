def normalizar_texto(valor):
    return (valor or "").strip().upper()


def es_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"
    """Limpia espacios y deja nombres en formato título."""
    return (valor or "").strip().title()


def es_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"
