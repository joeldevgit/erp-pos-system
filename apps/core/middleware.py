from .correlation import new_correlation_id, set_correlation_id, reset_correlation_id


class CorrelationIdMiddleware:
    """
    Agrega un correlation/request id a cada request para conectar logs,
    auditoría, errores Sentry y respuestas HTTP.
    """

    header_name = "HTTP_X_CORRELATION_ID"
    response_header_name = "X-Correlation-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming_id = request.META.get(self.header_name) or request.META.get("HTTP_X_REQUEST_ID")
        correlation_id = set_correlation_id(incoming_id or new_correlation_id())
        request.correlation_id = correlation_id
        request.request_id = correlation_id
        try:
            response = self.get_response(request)
            response[self.response_header_name] = correlation_id
            return response
        finally:
            reset_correlation_id()
