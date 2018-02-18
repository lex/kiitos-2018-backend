from .models import ObservationPoint, Observation
from rest_framework import serializers
import datetime


class ObservationPointSerializer(serializers.ModelSerializer):
    latest_observation = serializers.SerializerMethodField()

    class Meta:
        model = ObservationPoint
        fields = ('id',
                  'name',
                  'latitude',
                  'longitude',
                  'latest_observation', )

    def get_latest_observation(self, obj):
        latest_observation = obj.observation_set.last()

        if not latest_observation:
            return None

        s = ObservationSerializer(latest_observation)
        return s.data


class ObservationPointDetailsSerializer(serializers.ModelSerializer):
    observations = serializers.SerializerMethodField()

    class Meta:
        model = ObservationPoint
        fields = ('id', 'name', 'latitude', 'longitude', 'observations', )

    def get_observations(self, obj):
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        s = ObservationSerializer(
            obj.observation_set.filter(timestamp__gte=date_from).all(),
            many=True)
        return s.data


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ('temperature', 'timestamp', )
