from django.http import HttpResponse
from django.shortcuts import render
from file_upload import upload
from django.views.decorators.csrf import csrf_exempt
from trainings.models import Training, Track
from django.shortcuts import render_to_response
from math import hypot, sqrt
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
    colories = minutes * 9

    training_data = []
    for i,t in enumerate(track):
        if i == 0:
            distance = 0
            actual_speed = 0
        else:
            distance = hypot(track[i].lat - track[i-1].lat, track[i].lng - track[i-1].lng)
            actual_speed = distance/(track[i].time - track[i-1].time)
        training_data.append(dict(lat=t.lat, lng=t.lng, act_timestamp=t.time, dist=distance, speed=actual_speed))

    return render_to_response('trainings/view.html', {"track": training_data, "training_id": training_id,
                                                      "training": training, "duration": duration,
                                                      "calories": colories})