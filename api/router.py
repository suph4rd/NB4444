from rest_framework import routers

from B4 import models as b4_models
from api import views, serializers

router = routers.SimpleRouter()
router.register('default-deduction', views.DefaultDeductionListFilterModelViewSet)
router.register(
    'note',
    views.made_list_filter_model_viewset_class(
        b4_models.Note,
        serializers.get_model_serializer_class(
            b4_models.Note,
            local_exclude=['created_at', 'updated_at']
        )
    )
)
router.register(
    'plan',
    views.PlanModelListFilterModelViewSet
)
router.register(
    'task',
    views.TaskModelListFilterModelViewSet
)
