import threading

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_bot_info_view(request):
    from botV4 import main
    t1 = threading.Thread(target=main.receive_records_from_telegramm_bot)
    t1.start()
    return Response(status=status.HTTP_200_OK)
