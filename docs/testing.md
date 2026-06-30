# Testing

## Objetivo

El proyecto exige una cobertura mínima de **90%** para proteger la lógica crítica del ERP/POS.

## Comando local

```bash
pip install -r requirements/test.txt
pytest
```

## Cobertura obligatoria

La regla está en `pytest.ini`:

```ini
--cov=apps --cov-config=.coveragerc --cov-report=term-missing --cov-fail-under=90
```

Si la cobertura baja de 90%, el pipeline falla.

## Qué se prueba

- Services de productos e inventario.
- UseCases de creación, actualización y cambio de estado.
- Selectors.
- Permisos por rol.
- API v1.
- Auditoría.
- Casos límite como stock insuficiente y cantidad inválida.

## Regla de arquitectura

Las pruebas deben validar comportamiento de negocio, no solo que una URL responda.
