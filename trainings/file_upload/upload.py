__author__ = 'michalos'
import time
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from trainings.models import Training, Track
import json

def save_file(f):
    actual_time = int(time.time())
    filename = "{}/data/data_{}.json".format(settings.BASE_DIR, actual_time)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    jsonData = open(filename)
    data = json.load(jsonData)
    login = data['login']
    u = User.objects.get(username=login)
    print(data["points"][0]["time"], data["points"][-1]["time"], (data["points"][0]["time"]-data["points"][-1]["time"]))
    training = Training.objects.create(date_start=datetime.utcfromtimestamp(data["points"][0]["time"]/1000),
                                       date_end=datetime.utcfromtimestamp(data["points"][-1]["time"]/1000),
                                       duration=(data["points"][-1]["time"]-data["points"][0]["time"]),user=u)
    last_id = Training.objects.latest('id')
    for point in data['points']:
        print point
        Track.objects.create(training=last_id, lat=point['lat'], lng=point['lng'], time=point['time'])