from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        return render(request, 'homepage.html', {
            'new_song_name': request.POST.get('song_name', '')
        })
    return render(request, 'homepage.html')