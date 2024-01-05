from django.contrib import admin
from .models import Day, Train, TrainRun, Schedule, Route


admin.site.register(Train)
admin.site.register(TrainRun)
admin.site.register(Schedule)
admin.site.register(Route)
