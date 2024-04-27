from django.shortcuts import render
from rest_framework import viewsets

from auth.auth import IsPengurus
from events.models import Event
from events.v1.serializers import EventSerializer

