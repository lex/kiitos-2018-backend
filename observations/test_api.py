from django.test import TestCase
from .models import ObservationPoint, Observation
from .views import list_observation_points, show_observation_point_details, add_observation
from rest_framework.test import APIRequestFactory


class ListObservationPointsTests(TestCase):
    def setUp(self):
        point = ObservationPoint.objects.create(name='Tokyo',
                                                latitude=10.0,
                                                longitude=11.0)
        Observation.objects.create(observation_point=point, temperature=273.15)
        Observation.objects.create(observation_point=point, temperature=274.15)
        Observation.objects.create(observation_point=point, temperature=275.15)

        point = ObservationPoint.objects.create(name='Helsinki',
                                                latitude=12.0,
                                                longitude=13.0)
        Observation.objects.create(observation_point=point, temperature=273.15)
        Observation.objects.create(observation_point=point, temperature=274.15)
        Observation.objects.create(observation_point=point, temperature=275.15)

        self.factory = APIRequestFactory()

    def test_list_returns_200(self):
        request = self.factory.get('/observation-points/')
        response = list_observation_points(request)
        self.assertEqual(response.status_code, 200)

    def test_list_returns_all_points(self):
        request = self.factory.get('/observation-points/')
        response = list_observation_points(request)
        self.assertEqual(len(response.data), 2)


class ShowObservationPointDetailsTests(TestCase):
    def setUp(self):
        point = ObservationPoint.objects.create(name='Tokyo',
                                                latitude=10.0,
                                                longitude=11.0)
        Observation.objects.create(observation_point=point, temperature=273.15)
        Observation.objects.create(observation_point=point, temperature=274.15)
        Observation.objects.create(observation_point=point, temperature=275.15)

        self.point = point

        self.factory = APIRequestFactory()

    def test_details_returns_200_on_valid_point(self):
        request = self.factory.get('/observation-points/{}/'.format(
            self.point.id))
        response = show_observation_point_details(request, pk=self.point.id)
        self.assertEqual(response.status_code, 200)

    def test_details_returns_404_on_invalid_point(self):
        id = self.point.id + 50
        request = self.factory.get('/observation-points/{}/'.format(id))
        response = show_observation_point_details(request, pk=id)
        self.assertEqual(response.status_code, 404)


class AddObservationTests(TestCase):
    def setUp(self):
        point = ObservationPoint.objects.create(name='Tokyo',
                                                latitude=10.0,
                                                longitude=11.0)
        self.point = point

        self.factory = APIRequestFactory()

    def test_add_returns_200_on_valid_observation(self):
        data = {'point_id': self.point.id, 'temperature': 25.0}
        request = self.factory.post('/observations/', data, format='json')
        response = add_observation(request)
        self.assertEqual(response.status_code, 200)

    def test_add_returns_404_on_invalid_observation_point_id(self):
        data = {'point_id': self.point.id + 50, 'temperature': 25.0}
        request = self.factory.post('/observations/', data, format='json')
        response = add_observation(request)
        self.assertEqual(response.status_code, 404)

    def test_add_returns_400_on_invalid_observation_temperature(self):
        data = {'point_id': self.point.id, 'temperature': "asd"}
        request = self.factory.post('/observations/', data, format='json')
        response = add_observation(request)
        self.assertEqual(response.status_code, 400)

    def test_add_returns_400_on_negative_observation_temperature(self):
        data = {'point_id': self.point.id, 'temperature': "-1.0"}
        request = self.factory.post('/observations/', data, format='json')
        response = add_observation(request)
        self.assertEqual(response.status_code, 400)

    def test_add_adds_observation_to_observation_point(self):
        data = {'point_id': self.point.id, 'temperature': 512.0}
        request = self.factory.post('/observations/', data, format='json')
        response = add_observation(request)
        self.assertEqual(self.point.observation_set.last().temperature,
                         data['temperature'])
