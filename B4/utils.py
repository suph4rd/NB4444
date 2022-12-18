import locale

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from B4 import models

locale.setlocale(locale.LC_ALL, '')
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

now = timezone.now()


class PlanTask:
    plan_name = f"План на {now.strftime('%A, %d %B %Y')}"
    model = models.Plan

    @classmethod
    def create_today_plan(cls, user_id=None):
        user_list = cls._get_data_for_create(user_id)
        cls.model.objects.bulk_create(user_list)

    @classmethod
    def _get_data_for_create(cls, user_id):
        user_list = []
        qs_list = models.User.objects.all()
        if user_id:
            qs_list = qs_list.filter(pk=user_id)
        for user in qs_list:
            filters = {
                "name": cls.plan_name,
                "user": user
            }
            if not cls.model.objects.filter(**filters).exists():
                user_list.append(cls.model(**filters))
        return user_list


def made_login_required_generic_class(generic_class):
    """
    Make generic class with LoginRequiredMixin
    :param generic_class:
    :return: some of classes in django.views.generic
    """
    class LoginRequiredClass(LoginRequiredMixin, generic_class):
        pass
    return LoginRequiredClass
