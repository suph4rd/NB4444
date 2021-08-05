import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from B4 import utils


class Command(BaseCommand):

    def handle(self, *args, **options):
        utils.PlanTask.create_today_plan()
