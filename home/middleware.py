# core/middleware.py
import logging
import traceback
import uuid

from django.conf import settings
from django.http import JsonResponse, Http404
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ForceJsonErrorsMiddleware(MiddlewareMixin):
    """
    Force JSON for 404 and 500 (and convert any HTML 404 response to JSON).
    Requires DEBUG_PROPAGATE_EXCEPTIONS=True to catch 500s with DEBUG=True.
    Place FIRST in MIDDLEWARE.
    """

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Http404 as e:
            return self._json_404(request, e)
        except Exception as e:
            return self._json_500(request, e)

        # If a 404 slipped through as HTML (e.g., non-DRF view or default handler), normalize it here.
        if response.status_code == 404 and self._looks_like_html(response):
            return self._json_404(request, "The requested resource was not found.")

        return response

    def process_exception(self, request, exception):
        # Safety net (if __call__ doesn't catch due to some edge path)
        if isinstance(exception, Http404):
            return self._json_404(request, exception)
        return self._json_500(request, exception)

    # ---- helpers ----
    def _json_404(self, request, exc):
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": str(exc) or "The requested resource was not found.",
            "path": request.get_full_path(),
            "method": request.method,
        }, status=404)

    def _json_500(self, request, exc):
        error_id = str(uuid.uuid4())
        logger.exception("Unhandled exception (%s) on %s %s", error_id, request.method, request.get_full_path())
        payload = {
            "status": 500,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
            "path": request.get_full_path(),
            "method": request.method,
            "error_id": error_id,
        }
        if getattr(settings, "EXPOSE_DEBUG_TRACEBACK_IN_JSON", False) and settings.DEBUG:
            payload["debug"] = {
                "exception": repr(exc),
                "traceback": traceback.format_exc(),
            }
        return JsonResponse(payload, status=500)

    def _looks_like_html(self, response):
        ctype = (response.get("Content-Type") or "").lower()
        return "text/html" in ctype or "text/plain" in ctype