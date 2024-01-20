from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from . models import Musician

# Create your views here.

def AddMusician(request):
    if request.method == 'POST':
        musician_form = forms.MusicianForm(request.POST)
        if musician_form.is_valid():
            musician_form.save()
            return redirect('add_musician')
    
    else:
        musician_form = forms.MusicianForm()
    return render(request, 'musician/add_musician.html', {'form' : musician_form})


def editMusician(request, id):
    musician = Musician.objects.get(pk=id)
    musician_form = forms.MusicianForm(instance=musician)
    # print(musician.firstName)
    if request.method == 'POST':
        musician_form = forms.MusicianForm(request.POST, instance=musician)
        if musician_form.is_valid():
            musician_form.save()
            return redirect('homepage')
    
    return render(request, 'musician/add_musician.html', {'form' : musician_form})


def deleteMusician(request, id):
    musician = Musician.objects.get(pk=id)
    musician.delete()
    return redirect('homepage')
    