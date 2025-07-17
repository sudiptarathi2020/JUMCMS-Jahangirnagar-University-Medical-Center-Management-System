from core.jumcms.settings.base import MIDDLEWARE
from core.jumcms.settings.custom import IN_DOCKER
IN_DOCKER = str(IN_DOCKER).lower() == "true"
if IN_DOCKER:
    print("Running in Docker mode")
    assert MIDDLEWARE[:1] == [
        "django.middleware.security.SecurityMiddleware",
    ]