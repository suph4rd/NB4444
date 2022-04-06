import threading

from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import serializers
from api.permissions import IsSuperUserOrOwnerPermission
from B4 import models as b4_models


@api_view(['GET'])
def get_bot_info_view(request):
    from tele_bot import main
    t1 = threading.Thread(target=main.receive_records_from_telegramm_bot)
    t1.start()
    return Response(status=status.HTTP_200_OK)


class ListFilterModelViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrOwnerPermission, ]

    def get_int_value(self, value) -> int:
        match value:
            case int(value):
                return value
            case str(value) if value.isdigit() :
                return int(value)
            case list(value) if len(value) == 1:
                return self.get_int_value(value[0])
        raise ValueError({"error": f"{value} is not convent to Integer"})

    def list(self, request, *args, **kwargs):
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        if offset or limit:
            try:
                int_offset = self.get_int_value(offset)
                int_limit = self.get_int_value(limit)
                if int_offset and int_limit and int_offset >= int_limit:
                    raise ValueError(f"offset: {offset} больше либо равен limit: {limit}")
                self.queryset = self.queryset[int_offset: int_limit]
            except Exception as err:
                print(err)
                return Response({"error": str(err)}, status=400)
        return super().list(request, *args, **kwargs)


def made_list_filter_model_viewset_class(local_models, local_serializer, local_permission_classes: list = None):
    class CustomListFilterModelViewSet(ListFilterModelViewSet):
        queryset = local_models.objects.all()
        serializer_class = local_serializer
        if local_permission_classes:
            permission_classes = local_permission_classes
    return CustomListFilterModelViewSet


class DefaultDeductionListFilterModelViewSet(ListFilterModelViewSet):
    queryset = b4_models.DefaultDeductions.objects.all()
    serializer_class = serializers.get_model_serializer_class(
        b4_models.DefaultDeductions,
        local_exclude=['created_at', 'updated_at']
    )

    @action(methods=['get'], detail=False)
    def last(self, request, *args, **kwargs):
        qs = self.queryset.last()
        serializer = self.serializer_class(qs)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def user_last(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Пользователь не авторизован!"}, status=403)
        obj = self.queryset.filter(user=request.user).last()
        if not obj:
            return Response({}, status=404)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class CurrentSerializerMixin:
    model = None
    depth = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_class = self.get_current_serializer_class()

    def get_current_serializer_class(self, local_depth=None):
        return serializers.get_model_serializer_class(
            self.model,
            local_exclude=['created_at', 'updated_at'],
            local_depth=local_depth if isinstance(local_depth, int) else self.depth
        )

    def list(self, request, *args, **kwargs):
        if hasattr(self.model, 'user') and request.user.is_authenticated and not request.user.is_superuser:
            self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = self.get_current_serializer_class(local_depth=0)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = self.get_current_serializer_class(local_depth=0)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = self.get_current_serializer_class(local_depth=0)
        return super().partial_update(request, *args, **kwargs)


class PlanModelListFilterModelViewSet(CurrentSerializerMixin, ListFilterModelViewSet):
    model = b4_models.Plan
    queryset = model.objects.all()


class TaskModelListFilterModelViewSet(CurrentSerializerMixin, ListFilterModelViewSet):
    model = b4_models.Task
    queryset = model.objects.all()
    depth = 2

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            self.queryset = self.queryset.filter(plan__user=request.user)
        return super().list(request, *args, **kwargs)


class NoteModelListFilterModelViewSet(CurrentSerializerMixin, ListFilterModelViewSet):
    model = b4_models.Note
    queryset = model.objects.all()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Пользователь не авторизован!"}, status=403)
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    # @action(methods=['get'], detail=False)
    # def user_last(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return Response({"error": "Пользователь не авторизован!"}, status=403)
    #     obj = self.queryset.filter(user=request.user).last()
    #     if not obj:
    #         return Response({}, status=404)
    #     serializer = self.serializer_class(obj)
    #     return Response(serializer.data)
