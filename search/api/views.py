from itertools import chain
from operator import attrgetter

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.utils import json


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def search_view(request):
    if request.method == "POST":
        payload = {}
        data = {}
        count = 0

        query = request.data.get('q', None)
        if query is not None:
            if query is not "" and query is not " ":
                cabinets = Cabinet.objects.search(query)
                drawers = Drawer.objects.search(query)

                cabinets_serializer = ListCabinetSerializer(cabinets, many=True)
                drawers_serializer = DrawerSerializer(drawers, many=True)

                q_chain = chain(drawers_serializer.data, cabinets_serializer.data)
                new_l = list(q_chain)

                new_l.sort(key=lambda x: x['id'], reverse=False)

                payload['response'] = 'Successful'
                payload['data'] = new_l
            else:
                payload['response'] = 'Successful'
                payload['error_message'] = "Enter a text"

        return Response(payload)
