    (function() {
        const interval_name = JSON.parse(document.getElementById('user_name').textContent);
        const recorder_button = document.querySelector('.chords-notes-selector')
        const Note = document.querySelector('.note')
        const sharp_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#','G', 'G#'];
        const interval_time_length = 250
        const websocket_url = 'ws://'
                            + window.location.host
                            + '/ws/intervals/'
                            + interval_name.replace('.', '_')
                            + '/'

        let target_note = random_note(sharp_notes);
        let socket_paused = false;

        function random_note(notes) {
            return notes[Math.floor(Math.random() * notes.length)];
        }


        const intervals_websocket_functionality = {
            async init() {
                intervals_websocket_handlers.setup_event_listeners();
            },

        }

        const intervals_websocket_handlers = {
            async interval_listener() {
                /* 
                Send and audio chunks to server
                And receive decoded music note and frequency 
                */
            try {
                const stream = await navigator.mediaDevices.getUserMedia({audio:true})
                const socket = new WebSocket(websocket_url);

                socket.onopen = () => {
                    const stop_button = document.querySelector('.stop-interval-button');

                    Note.innerHTML = target_note;

                    const record_and_send = async(stream) => {
                        const recorder = new MediaRecorder(stream, {mimeType: 'audio/webm'});
                        const chunks = [];

                        recorder.ondataavailable = (e) => {
                            chunks.push(e.data);
                        };

                        recorder.onstop = (e) => {
                            if (socket.readyState == WebSocket.OPEN) {
                                socket.send(new Blob(chunks));
                            }
                        };

                        recorder.start();
                        setTimeout(() => recorder.stop(), interval_time_length);
                        
                        stop_button.onclick = (e) => {
                            socket.close();
                            recorder.stop();
                        };
                    };
                    
                    setInterval(() => { 
                        if(!socket_paused) {
                            record_and_send(stream); }}, interval_time_length);
            };

            socket.onclose = (message) => {
                console.log(message);
            };

            socket.onmessage = (message) => {
                const received = JSON.parse(message.data);
                if (received.message === target_note) {
                    Note.innerHTML = 'Correct!';
                }
                target_note = random_note(sharp_notes);
                socket_paused = true;
                setTimeout(() => {
                    Note.innerHTML = target_note;
                    socket_paused = false;
                }, 2000);

            };
            } catch (err) {
                    console.error(`${err.name}: ${err.message}`);
                }
            },
            setup_event_listeners() {
                recorder_button.addEventListener('click',this.interval_listener);
            }
        }

        intervals_websocket_functionality.init()

    })();
