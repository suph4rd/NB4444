from rest_framework import routers, permissions

from B4 import models as b4_models
from api import views, serializers

router = routers.SimpleRouter()
router.register('default-deduction', views.DefaultDeductionListFilterModelViewSet)
router.register(
    'note',
    views.NoteModelListFilterModelViewSet
)
router.register(
    'plan',
    views.PlanModelListFilterModelViewSet
)
router.register(
    'task',
    views.TaskModelListFilterModelViewSet
)
