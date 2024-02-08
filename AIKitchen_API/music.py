import os
import requests
import json
import base64
import logging

class Music:
    musiclm_url = "https://content-aisandbox-pa.googleapis.com/v1:soundDemo?alt=json"
    def get_tracks(self, input, generationCount, token):
        if not isinstance(generationCount, int):
            generationCount = 2
        generationCount = min(8, max(1, generationCount))

        payload = json.dumps({
        "generationCount": generationCount,
        "input": {
            "textInput": input
        },
        "soundLengthSeconds": 30  # this doesn't change anything 
        })

        headers = {
        'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.post(self.musiclm_url, headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            logging.error("Can't connect to the server.")
            # Bad Gateway
            return 502
        if response.status_code == 400:
                logging.error("Oops, can't generate audio for that.")
                # Bad Request
                return 400
        
        tracks = []
        for sound in response.json()['sounds']:
            tracks.append(sound["data"])

        return tracks

    def b64toMP3(self, tracks_list, filename):
        count = 0
        new_filename = filename
        while os.path.exists(new_filename):
            count += 1
            new_filename = f'{filename} ({count})'

        os.mkdir(new_filename)

        for i, track in enumerate(tracks_list):
            with open(f"{new_filename}/track{i+1}.mp3", "wb") as f:
                f.write(base64.b64decode(track))

        logging.info("Tracks successfully generated!")
        # Successful Request
        return 200