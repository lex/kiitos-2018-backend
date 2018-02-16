from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ObservationPoint, Observation
from .serializers import ObservationPointSerializer, ObservationSerializer, ObservationPointDetailsSerializer


@api_view(['GET'])
def list_observation_points(request, format=None):
    points = ObservationPoint.objects.all()
    serializer = ObservationPointSerializer(points, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_observation_point_details(request, pk, format=None):
    try:
        point = ObservationPoint.objects.get(pk=pk)
    except ObservationPoint.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ObservationPointDetailsSerializer(point)
    return Response(serializer.data)


@api_view(['POST'])
def add_observation(request, format=None):
    observation_point_id = request.data.get('point_id', -1)

    try:
        point = ObservationPoint.objects.get(pk=observation_point_id)
    except ObservationPoint.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {'temperature': request.data.get('temperature', None)}

    serializer = ObservationSerializer(data=data)

    if serializer.is_valid():
        serializer.save(observation_point=point)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
