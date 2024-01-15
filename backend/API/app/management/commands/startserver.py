from django.core.management.base import BaseCommand
from django.core.management import call_command
from project.settings.dev_settings import DEFAULT_IP, DEFAULT_PORT

class Command(BaseCommand):
    help = 'Run the Django development server using environment variables for IP and port'

    def handle(self, *args, **kwargs):
        call_command('runserver', f'{DEFAULT_IP}:{DEFAULT_PORT}')
