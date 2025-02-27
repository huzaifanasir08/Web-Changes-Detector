from django.core.management.base import BaseCommand
from ...task import run_auto_check

class Command(BaseCommand):
    help = 'Runs the background task'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting background task...'))
        run_auto_check()


