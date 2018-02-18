from django.test import TestCase
from observations.models import ObservationPoint, Observation


class ObservationPointTests(TestCase):
    def setUp(self):
        point = ObservationPoint.objects.create(name='Tokyo',
                                                latitude=10.0,
                                                longitude=11.0)
        Observation.objects.create(observation_point=point, temperature=273.15)
        Observation.objects.create(observation_point=point, temperature=274.15)
        Observation.objects.create(observation_point=point, temperature=275.15)

    def test_point_has_three_observations(self):
        point = ObservationPoint.objects.get(name='Tokyo')
        self.assertEqual(len(point.observation_set.all()), 3)
