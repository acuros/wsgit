from django.core.management.base import BaseCommand, CommandError
from imdjango.network.server import Server

class Command(BaseCommand):
    def handle(self, *args, **options):
        Server.start_server()
