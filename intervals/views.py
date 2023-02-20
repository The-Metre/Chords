from django.shortcuts import render

# Create your views here.

def fretboard(request):
    return render(request, 'fretboard.html')