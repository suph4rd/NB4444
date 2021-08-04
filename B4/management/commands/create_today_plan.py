import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from B4 import models

today = datetime.date.today()


class Command(BaseCommand):
    plan_name = f"План на {today.strftime('%A, %d %B %Y')}"
    model = models.Plan

    def handle(self, *args, **options):
        user_list = self.get_data_for_create()
        print(user_list)
        self.model.objects.bulk_create(user_list)

    def get_data_for_create(self):
        user_list = []
        for user in User.objects.all():
            if not self.model.objects.filter(created_at__date=today).exists():
                user_list.append(
                    self.model(
                        name=self.plan_name,
                        user=user
                    )
                )
        return user_list
