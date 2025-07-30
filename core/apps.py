from django.apps import AppConfig
import sys

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        skip_commands = ['makemigrations', 'migrate', 'collectstatic', 'shell', 'createsuperuser', 'dbshell', 'test']
        if any(cmd in sys.argv for cmd in skip_commands):
            return

        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Empleado')
