import json
import logging

from apps.core.correlation import set_correlation_id, reset_correlation_id
from apps.core.logging import JsonFormatter


def test_json_formatter_incluye_correlation_id():
    set_correlation_id("cid-test")
    try:
        record = logging.LogRecord("test", logging.INFO, __file__, 1, "hola", None, None)
        payload = json.loads(JsonFormatter().format(record))
        assert payload["correlation_id"] == "cid-test"
        assert payload["message"] == "hola"
    finally:
        reset_correlation_id()
