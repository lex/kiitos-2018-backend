from django.db import models


class ObservationPoint(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Observation(models.Model):
    observation_point = models.ForeignKey(ObservationPoint,
                                          on_delete=models.PROTECT,
                                          editable=False)

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    # in kelvin
    temperature = models.DecimalField(max_digits=20,
                                      decimal_places=10,
                                      editable=False, )
