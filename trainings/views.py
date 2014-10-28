from django.http import HttpResponse
from django.shortcuts import render
from file_upload import upload
from django.views.decorators.csrf import csrf_exempt
from trainings.models import Training, Track
from django.shortcuts import render_to_response
from math import cos, sin, acos, pi, sqrt
# Create your views here.

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        upload.save_file(request.FILES['uploaded_file'])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=301)
        #upload(name)

def view_training(request, training_id):
    track = Track.objects.filter(training = training_id)
    training = Training.objects.get(id = training_id)

    x = training.duration / 1000
    seconds = x % 60
    x /= 60
    minutes = x % 60
    duration = "{0} min {1} sec".format(minutes, seconds)
    calories = minutes * 9

    training_data = []
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
            delta_time = (track[i].time - track[i-1].time)/1000
            actual_speed = distance/(delta_time)

        training_data.append(dict(lat=t.lat, lng=t.lng, act_timestamp=t.time, delta_time=delta_time,
                                  dist=distance, speed=actual_speed))

    avg_speed = training.distance / (training.duration/1000)
    return render_to_response('trainings/view.html', {"track": training_data, "training_id": training_id,
                                                      "training": training, "duration": duration,
                                                      "calories": calories, "whole_distance": training.distance,
                                                      "avg_speed": avg_speed, "max_speed": training.max_speed})