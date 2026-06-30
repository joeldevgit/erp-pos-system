# Coverage real mayor a 90%

El proyecto tiene umbral obligatorio en `pytest.ini`:

```ini
addopts = -v --cov=apps --cov-config=.coveragerc --cov-report=term-missing --cov-fail-under=90
```

Ejecución comprobada:

```bash
python -m pytest -q
```

Resultado local después de las mejoras:

```text
39 passed, 1 skipped
TOTAL 95.17%
Required test coverage of 90% reached.
```

La prueba E2E queda marcada como `e2e`; si no está instalado Chromium, puede omitirse en ambientes rápidos de CI. Para ejecutarla completa:

```bash
playwright install chromium
pytest tests/e2e --e2e
```
