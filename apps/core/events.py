from dataclasses import dataclass
from datetime import datetime
from django.utils import timezone


@dataclass
class DomainEvent:
    nombre: str
    data: dict
    fecha: datetime = None

    def __post_init__(self):
        if self.fecha is None:
            self.fecha = timezone.now()



_listeners = {}


def registrar_listener(nombre_evento, funcion):
    if nombre_evento not in _listeners:
        _listeners[nombre_evento] = []

    _listeners[nombre_evento].append(funcion)


def publicar_evento(evento):
    listeners = _listeners.get(evento.nombre, [])

    for listener in listeners:
        listener(evento)