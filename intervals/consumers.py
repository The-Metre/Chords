import json

from channels.generic.websocket import WebsocketConsumer
from pocket_chords.models import (
    ChordNotesRelation, Chord, MusicNote
)

class IntervalConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chord = ChordNotesRelation.objects.filter(chord_name=Chord.objects.get(name=message))
        unswer = ' '.join(note.chord_note.name for note in chord)
        self.send(text_data=json.dumps({'message': unswer}))