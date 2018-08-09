from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from AMD.music.models import Document
from AMD.music.forms import DocumentForm

from AMD.music.dictation import convert

import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)

def home(request):
    documents = Document.objects.all()
    return render(request, 'music/home.html', { 'documents': documents })


def converter(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(clean_filename(myfile.name), myfile)
        uploaded_file_url = fs.url(filename)

        convert(uploaded_file_url)

        return render(request, 'music/converter.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'music/converter.html')


def record(request): #httprequest client
    return render(request, 'music/record.html')

def play(request): #httprequest client
    return render(request, 'music/play.html')

