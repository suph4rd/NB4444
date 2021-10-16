import threading

from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from B4 import models as b4_models
from api import serializers


@api_view(['GET'])
def get_bot_info_view(request):
    from botV4 import main
    t1 = threading.Thread(target=main.receive_records_from_telegramm_bot)
    t1.start()
    return Response(status=status.HTTP_200_OK)


class ListFilterModelViewSet(ModelViewSet):

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


class DefaultDeductionListFilterModelViewSet(ListFilterModelViewSet):
    queryset = b4_models.DefaultDeductions.objects.all()
    serializer_class = serializers.get_model_serializer(
        b4_models.DefaultDeductions,
        local_exclude=['created_at', 'updated_at']
    )

    @action(methods=['get'], detail=False)
    def last(self, request, *args, **kwargs):
        qs = self.queryset.last()
        serializer = self.serializer_class(qs)
        return Response(serializer.data)


class NoteModelListFilterModelViewSet(ListFilterModelViewSet):
    queryset = b4_models.Note.objects.all()
    serializer_class = serializers.get_model_serializer(
        b4_models.Note,
        local_exclude=['created_at', 'updated_at']
    )
