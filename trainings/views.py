from django.http import HttpResponse
from django.shortcuts import render
from file_upload import upload
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        upload.save_file(request.FILES['uploaded_file'])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=301)
        #upload(name)