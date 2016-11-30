from django.shortcuts import render
from rest_framework import generics
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from common.mongo import mongodb_get_data

# Create your views here.


class DataListView(generics.CreateAPIView):
    queryset = []
    serializer_class = Serializer

    def post(self, request, *args, **kwargs):
        uuid = request.data.get('uuid')
        item = request.data.get('item')
        start_time = request.data.get('start')
        end_time = request.data.get('end')

        data = mongodb_get_data(uuid, start_time, end_time, item)

        return Response(data)
