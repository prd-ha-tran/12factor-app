"""A config to pass into gunicorn as a python module.
In order to work, `DJANGO_SETTINGS_MODULE` env var must be set first.
"""

from django.conf import settings

locals().update(settings.GUNICORN_CONFIGS)
