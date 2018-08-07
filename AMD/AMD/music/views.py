from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from AMD.music.models import Document
from AMD.music.forms import DocumentForm


def home(request):
    documents = Document.objects.all()
    return render(request, 'music/home.html', { 'documents': documents })


def converter(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'music/converter.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'music/converter.html')


def record(request): #httprequest client
    return render(request, 'music/record.html')

def play(request): #httprequest client
    return render(request, 'music/play.html')