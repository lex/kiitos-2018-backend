from django.contrib import admin

from .models import ObservationPoint, Observation

admin.site.register(ObservationPoint)
admin.site.register(Observation)
