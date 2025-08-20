from rest_framework.views import exception_handler as drf_default_handler
from rest_framework.response import Response

def drf_exception_handler(exc, context):
    response = drf_default_handler(exc, context)
    if response is None:
        return None
    request = context.get("request")
    return Response({
        "status": response.status_code,
        "error": _status_text(response.status_code),
        "message": _best_message(response.data),
        "details": response.data if isinstance(response.data, dict) else None,
        "path": request.get_full_path() if request else None,
        "method": request.method if request else None,
    }, status=response.status_code)

def _status_text(code):
    return {
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
        404: "Not Found", 405: "Method Not Allowed", 415: "Unsupported Media Type",
        429: "Too Many Requests", 500: "Internal Server Error",
    }.get(code, "Error")

def _best_message(data):
    if isinstance(data, dict):
        if isinstance(data.get("detail"), str):
            return data["detail"]
        for v in data.values():
            if isinstance(v, str): return v
            if isinstance(v, list) and v and isinstance(v[0], str): return v[0]
    if isinstance(data, list) and data and isinstance(data[0], str):
        return data[0]
    return "Request could not be processed."