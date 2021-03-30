from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Hour
from .models import DiscordUser as DiscordUserModel
from .serializer import (DiscordUserSerializer, HourSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F


import requests
import json
import re

class DiscordUsers(generics.ListCreateAPIView):
    queryset = DiscordUserModel.objects.all()
    serializer_class = DiscordUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'code', 'name']

class DiscordUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscordUserModel.objects.all()
    serializer_class = DiscordUserSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))


class HoursAPIView(generics.ListCreateAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer

class HourAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

class HourByCodeAPIView(APIView):

    def get(self, request, code):
        code = ''.join(re.findall(r'[0-9]+', code))
        user_obj = get_object_or_404(DiscordUserModel.objects.all(), code=code)
        pk = get_object_or_404(DiscordUserModel.objects.all(), code=code).id
        hour_obj = get_object_or_404(Hour.objects.all(), id=pk)
        return Response({
            "name" : user_obj.name,
            "minutes" : hour_obj.minutes
        })

class HitMinuteAPIView(generics.RetrieveAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer

    def retrieve(self, request, pk):
        instance = self.get_object()
        Hour.objects.filter(pk=instance.id).update(minutes=F('minutes') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class HitMinuteByCodeAPIView(APIView):
    def get(self, request, code):
        code = ''.join(re.findall(r'[0-9]+', code))
        pk = get_object_or_404(DiscordUserModel.objects.all(), code=code).id
        Hour.objects.filter(id=pk).update(minutes=F('minutes') + 1)
        obj = get_object_or_404(Hour.objects.all(), id=pk)
        return Response({
            'minutes' : obj.minutes
        })
