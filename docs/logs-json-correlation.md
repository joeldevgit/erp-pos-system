# Logs JSON y Correlation ID

Se agregó:

- `apps.core.middleware.CorrelationIdMiddleware`
- `apps.core.correlation`
- `apps.core.logging.JsonFormatter`
- header de respuesta `X-Correlation-ID`

Cada log sale en JSON con:

```json
{
  "timestamp": "...",
  "level": "INFO",
  "logger": "...",
  "message": "...",
  "correlation_id": "..."
}
```

Variables útiles:

```env
LOG_FORMAT=json
LOG_LEVEL=INFO
```

Si el cliente envía `X-Correlation-ID`, el sistema lo reutiliza. Si no, genera uno nuevo.
