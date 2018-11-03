from django.shortcuts import render
from django.http import HttpResponse
from Application.functions import handle_uploaded_file, clear_media
from Application.forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'Application/index.html')
def about(request):
    return render(request,'Application/about.html')

def upload(request):
    if request.method == 'POST':
        clear_media()
        form = UploadFileForm(request.FILES)
        fs = FileSystemStorage()
        myfile = request.FILES['file']
        filename = fs.save(myfile.name, myfile)
        # print(type(filename), filename)
        # return new file
        if filename.endswith('.mp4'):
            handle_uploaded_file('media/' + filename)
            output_file = 'output.mp4'
            return render(request, "Application/download.html", {'output': output_file})

        elif filename.endswith('.jpeg') or filename.endswith('jpg') or filename.endswith('png'):
            handle_uploaded_file('media/' + filename)
            output_file = 'output_image.jpg'
            return render(request, "Application/download.html", {'output': output_file})
        else:
            return render(request, "Application/upload_error.html")
    else:
        form = UploadFileForm()
        return render(request, "Application/upload.html", {'form': form})
