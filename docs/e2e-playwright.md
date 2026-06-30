# Suite E2E con Playwright

Archivo principal:

```text
tests/e2e/test_smoke_playwright.py
```

Cubre navegador real sobre:

- `/health/`
- `/live/`
- `/ready/`
- `/api/v2/status/`

Ejecución local:

```bash
pip install -r requirements/test.txt
playwright install chromium
pytest tests/e2e --e2e --no-cov
```

Nota: la suite principal (`pytest`) deja los E2E en `skip` por defecto para no romper entornos donde Chromium no está instalado. En CI se instala Chromium y se ejecuta `pytest tests/e2e --e2e --no-cov` como paso separado.
