from django.shortcuts import render
from musician.models import Musician
from album.models import Album

def Home(request):
    data_with_album = []
    # data_album = Album.objects.all()
    musicians = Musician.objects.all()

    for musician in musicians:
        album = Album.objects.filter(musician = musician)
        data_with_album.append({'musician': musician, 'album': album})

    return render(request, 'index.html', {'data': data_with_album})