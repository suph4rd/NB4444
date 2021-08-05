import datetime
from django.contrib.auth.models import User

from B4 import models
import locale

locale.setlocale(locale.LC_ALL, '')
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
today = datetime.date.today()


class PlanTask(object):
    plan_name = f"План на {today.strftime('%A, %d %B %Y')}"
    model = models.Plan

    @classmethod
    def create_today_plan(cls, user_id=None):
        user_list = cls._get_data_for_create(user_id)
        cls.model.objects.bulk_create(user_list)

    @classmethod
    def _get_data_for_create(cls, user_id):
        user_list = []
        qs_list = User.objects.filter(pk=user_id) if user_id else User.objects.all()
        for user in qs_list:
            filters = {
                "name": cls.plan_name,
                "user": user
            }
            if not cls.model.objects.filter(**filters).exists():
                user_list.append(cls.model(**filters))
        return user_list
