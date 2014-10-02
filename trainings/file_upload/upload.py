__author__ = 'michalos'
import time
from django.conf import settings
import json

def save_file(f):
    actual_time = int(time.time())
    filename = "{}/data/data_{}.json".format(settings.BASE_DIR, actual_time)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    jsonData = open(filename)
    data = json.load(jsonData)