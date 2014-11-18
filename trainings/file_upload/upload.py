__author__ = 'michalos'
import time
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from trainings.models import Training, Track
import json
from math import cos, sin, acos
from django.http import HttpResponse

def save_file(f):
    actual_time = int(time.time())
    filename = "{}/data/data_{}.json".format(settings.BASE_DIR, actual_time)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    jsonData = open(filename)
    data = json.load(jsonData)

    u = authenticate(username=data['login'], password=data['password'])
    if u is None:
        return 1

    try:
        data['points']
    except KeyError:
        return 2

    print(data["points"][0]["time"], data["points"][-1]["time"], (data["points"][0]["time"]-data["points"][-1]["time"]))
    training = Training.objects.create(date_start=datetime.utcfromtimestamp(data["points"][0]["time"]/1000),
                                       date_end=datetime.utcfromtimestamp(data["points"][-1]["time"]/1000),
                                       duration=(data["points"][-1]["time"]-data["points"][0]["time"]),user=u)
    last_id = Training.objects.latest('id')
    whole_distance = 0
    max_speed = 0
    pk = 180/3.14169
    for i, point in enumerate(data['points']):
        print point
        if i == 0:
            distance = 0
            actual_speed = 0
            delta_time = 0
        else:
            x1 = float(prev_point['lat']) / pk
            y1 = float(prev_point['lng']) / pk
            x2 = float(point['lat']) / pk
            y2 = float(point['lng']) / pk

            t1 = cos(x1)*cos(y1)*cos(x2)*cos(y2)
            t2 = cos(x1)*sin(y1)*cos(x2)*sin(y2)
            t3 = sin(x1)*sin(x2)
            distance = acos(t1 + t2 + t3) * 6366000

            whole_distance = whole_distance + distance
            delta_time = (point['time'] - prev_point['time'])/1000
            actual_speed = distance/(delta_time)
            if actual_speed > max_speed:
                max_speed = actual_speed
        Track.objects.create(training=last_id, lat=point['lat'], lng=point['lng'], time=point['time'] )
        prev_point = point
    training.distance = whole_distance
    training.max_speed = max_speed
    training.save()
    return 0