from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "simpleapp"

    def ready(self):
        import simpleapp.signals


red = redis.Redis(
    host='redis-16337.c302.asia-northeast1-1.gce.cloud.redislabs.com',
    port=16337,
    password='DDBmamFUMAbrb7Ck68Q0tODPNDF6Cf3z'
)