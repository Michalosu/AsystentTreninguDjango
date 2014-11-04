__author__ = 'michalos'
import time
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from trainings.models import Training, Track
import json
from math import cos, sin, acos

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
            x1 = float(point[i-1].lat) / pk
            y1 = float(point[i-1].lng) / pk
            x2 = float(point[i].lat) / pk
            y2 = float(point[i].lng) / pk

            t1 = cos(x1)*cos(y1)*cos(x2)*cos(y2)
            t2 = cos(x1)*sin(y1)*cos(x2)*sin(y2)
            t3 = sin(x1)*sin(x2)
            distance = acos(t1 + t2 + t3) * 6366000
            whole_distance = whole_distance + distance
            delta_time = (point[i].time - point[i-1].time)/1000
            actual_speed = distance/(delta_time)
            if actual_speed > max_speed:
                max_speed = actual_speed
        Track.objects.create(training=last_id, lat=point['lat'], lng=point['lng'], time=point['time'] )


def calculate_stats(duration):
    training_data = []
    whole_distance = 0
    max_speed = 0
    pk = 180/3.14169
    for i,t in enumerate(track):
        if i == 0:
            distance = 0
            actual_speed = 0
            delta_time = 0
        else:
            x1 = float(track[i-1].lat) / pk
            y1 = float(track[i-1].lng) / pk
            x2 = float(track[i].lat) / pk
            y2 = float(track[i].lng) / pk

            t1 = cos(x1)*cos(y1)*cos(x2)*cos(y2)
            t2 = cos(x1)*sin(y1)*cos(x2)*sin(y2)
            t3 = sin(x1)*sin(x2)
            distance = acos(t1 + t2 + t3) * 6366000
            whole_distance = whole_distance + distance
            delta_time = (track[i].time - track[i-1].time)/1000
            actual_speed = distance/(delta_time)
            if actual_speed > max_speed:
                max_speed = actual_speed
        training_data.append(dict(lat=t.lat, lng=t.lng, act_timestamp=t.time, delta_time=delta_time,
                                  dist=distance, speed=actual_speed))
    avg_speed = whole_distance / (duration/1000)