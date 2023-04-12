import json
import os 

from channels.generic.websocket import AsyncWebsocketConsumer
from io import BytesIO
from pydub import AudioSegment

import wave
from project_tools.tuner import *

TEMPORAL_AUDIO_FILE = 'temp.wav'

class IntervalConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["user_name"]
        self.room_group_name = "chords_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        if os.path.exists(TEMPORAL_AUDIO_FILE):
                os.remove(TEMPORAL_AUDIO_FILE)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        audio_file = AudioSegment.from_file(BytesIO(bytes_data))
        temp_wav = TEMPORAL_AUDIO_FILE
        audio_file.export(temp_wav, format='wav')

        try:
            with wave.open(temp_wav, 'rb') as file:
                freq = find_max_frequency(file)
                if freq:
                    tone = get_closest_note(freq)
                    print(tone)

                    await self.channel_layer.group_send(self.room_group_name, \
                                            {'type': 'chords_message', \
                                             'message': tone[0]})
        except struct.error as error:
            print(error)

        

    async def chords_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))