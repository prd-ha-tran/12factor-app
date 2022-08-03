import time

from django.conf import settings
from django.http import HttpRequest, HttpResponse


def waiting_view(request: HttpRequest):
    if 'for' in request.GET:
        secs = int(request.GET['for'])
    else:
        secs = settings.WAIT_SECS
    time.sleep(secs)
    return HttpResponse(f"You've waited for {secs} second(s).")


def error_view(request: HttpRequest):
    raise ValueError("catch me if you can")
