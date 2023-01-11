from django.shortcuts import render, redirect
from pocket_chords.models import Song

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        # Check if 'name' space is not empty 
        if request.POST['song_name']:
            Song.objects.create(name=request.POST['song_name'], text='')
            return redirect('/song_list/something_right_here/')

    songs = Song.objects.all()
    return render(request, 'homepage.html', {
        'songs' : songs
    })

def song_list(request):
    """ Show the user song list """  
    pass
    songs = Song.objects.all()
    return render(request, 'homepage.html', {
        'songs' : songs
    })