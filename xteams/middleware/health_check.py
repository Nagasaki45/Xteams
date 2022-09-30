from django.http import HttpResponse


def health_check_middleware(get_response):
    def middleware(request):
        if request.path == "/health":
            return HttpResponse("OK")
        return get_response(request)
    return middleware