from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register('default-deduction', views.DefaultDeductionListFilterModelViewSet)
router.register('note', views.NoteModelListFilterModelViewSet)
