from django.core.management.base import BaseCommand, CommandError
from imdjango.network.server import IMServer

class Command(BaseCommand):
    def handle(self, *args, **options):
        IMServer.start_server(*args)
