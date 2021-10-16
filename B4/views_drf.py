from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_bot_info(request):
    from botV4 import main
    main.main()
    return Response(status=status.HTTP_200_OK)