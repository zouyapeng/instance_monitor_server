from django.shortcuts import render
from rest_framework import generics
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from common.mongo import mongodb_get_data

# Create your views here.


ITEM = ['cpu usage', 'memory usage', 'disk read speed', 'disk write speed', 'incoming network traffic', 'outgoing network traffic']


class DataListView(generics.CreateAPIView):
    queryset = []
    serializer_class = Serializer

    def post(self, request, *args, **kwargs):
        uuid = request.data.get('uuid', None)
        item = request.data.get('item', None)
        start_time = request.data.get('start', None)
        end_time = request.data.get('end', None)

        if uuid is None:
            return Response(data={'messages': 'uuid is need for get vm Data!'}, status=400)

        if item and item not in ITEM:
            return Response(data={'messages': 'item is not correct!'}, status=400)

        if item and start_time is None:
            return Response(data={'messages': 'start is need for get vm Data if item is specified!'}, status=400)

        try:
            data = mongodb_get_data(uuid, start_time, end_time, item)
        except Exception as error:
            return Response(data={'messages': 'Bad Request!', 'error': str(error)}, status=400)

        return Response(data)
