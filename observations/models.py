from django.db import models


def kelvin_to_celsius(kelvin):
    return float(kelvin) - 273.15


class ObservationPoint(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.name


class Observation(models.Model):
    observation_point = models.ForeignKey(ObservationPoint,
                                          on_delete=models.PROTECT, )

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    # in kelvin
    temperature = models.DecimalField(max_digits=20, decimal_places=10, )

    def __str__(self):
        return '{} at {} - {} C'.format(self.observation_point.name,
                                        self.timestamp,
                                        kelvin_to_celsius(self.temperature))
