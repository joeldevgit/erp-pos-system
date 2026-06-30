# Health, Ready y Live

Endpoints operativos para despliegues productivos:

- `GET /health/`: health general para monitores externos.
- `GET /live/`: liveness probe; confirma que el proceso Django responde.
- `GET /ready/`: readiness probe; valida base de datos y cache antes de recibir tráfico.

Respuesta esperada:

```json
{
  "status": "ready",
  "service": "myerpposdj",
  "checks": {
    "database": "ok",
    "cache": "ok"
  }
}
```

Uso recomendado:

- Kubernetes/Docker: usar `/live/` como liveness probe.
- Load balancer/Render/UptimeRobot: usar `/health/`.
- Antes de enviar tráfico real: usar `/ready/`.
