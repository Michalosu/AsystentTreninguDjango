from django.http import HttpResponse
from django.shortcuts import render
from file_upload import upload
from django.views.decorators.csrf import csrf_exempt
from trainings.models import Training, Track
from django.shortcuts import render_to_response
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
    return render_to_response('trainings/view.html', {"track": track})