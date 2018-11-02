from django.shortcuts import render
from django.http import HttpResponse
from Application.functions import handle_uploaded_file
from Application.forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'Application/index.html')
def about(request):
    return render(request,'Application/about.html')

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.FILES)
        fs = FileSystemStorage()
        myfile = request.FILES['file']
        filename = fs.save(myfile.name, myfile)
        # print(type(filename), type(file))
        # return new file
        handle_uploaded_file('media/' + filename)
        output_file = 'video.mp4'
        return render(request, "Application/download.html", {'output': output_file})
    else:
        form = UploadFileForm()
        return render(request, "Application/upload.html", {'form': form})
