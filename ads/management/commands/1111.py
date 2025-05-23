from django.utils import timezone
from django.core.management import BaseCommand
from ads.models import Advertisement

 
def ff():
    Advertisement.objects.filter(user=request.user).last()

class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()
