from django.test import TestCase
from observations.models import ObservationPoint, Observation
from observations.serializers import ObservationPointSerializer, ObservationPointDetailsSerializer, ObservationSerializer
import datetime


class ObservationPointSerializerTests(TestCase):
    def setUp(self):
        point = ObservationPoint.objects.create(name='Tokyo',
                                                latitude=10.0,
                                                longitude=11.0)
        Observation.objects.create(observation_point=point, temperature=273.15)
        Observation.objects.create(observation_point=point, temperature=274.15)
        Observation.objects.create(observation_point=point, temperature=275.15)

    def test_serializer_data_has_all_fields(self):
        point = ObservationPoint.objects.get(name='Tokyo')
        s = ObservationPointSerializer(point)

        fields = ['id', 'name', 'latitude', 'longitude', 'latest_observation']

        for key, v in s.data.items():
            self.assertEqual(key in fields, True)

    def test_serializer_data_has_correct_latest_observation(self):
        point = ObservationPoint.objects.get(name='Tokyo')
        observation = Observation.objects.create(observation_point=point,
                                                 temperature=276.15)
        s = ObservationPointSerializer(point)
        expected = observation.temperature
        temperature = float(s.data['latest_observation']['temperature'])

        self.assertEqual(temperature, observation.temperature)


class ObservationPointDetailsSerializerTests(TestCase):
    def setUp(self):
        point = ObservationPoint.objects.create(name='Tokyo',
                                                latitude=10.0,
                                                longitude=11.0)
        Observation.objects.create(observation_point=point, temperature=273.15)
        Observation.objects.create(observation_point=point, temperature=274.15)
        Observation.objects.create(observation_point=point, temperature=275.15)

    def test_serializer_data_has_all_observations_for_last_24_hours(self):
        point = ObservationPoint.objects.get(name='Tokyo')
        s = ObservationPointDetailsSerializer(point)

        self.assertEqual(len(s.data['observations']), 3)

    def test_serializer_data_doesnt_include_observations_older_than_24_hours(
            self):
        point = ObservationPoint.objects.get(name='Tokyo')
        o = Observation.objects.create(observation_point=point,
                                       temperature=275.15)
        o.timestamp = o.timestamp - datetime.timedelta(days=1)
        o.save()

        s = ObservationPointDetailsSerializer(point)

        self.assertEqual(len(s.data['observations']), 3)
