import requests
import pyaudio
import io
import base64
import json

# Shazam API endpoint and headers
shazam_url = 'https://shazam.p.rapidapi.com/songs/detect'
headers = {
    'content-type': 'text/plain',
    'X-RapidAPI-Key': 'ur api key here',
    'X-RapidAPI-Host': 'shazam.p.rapidapi.com'
}

def capture_audio():
    audio = pyaudio.PyAudio()
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 4
    
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("Recording audio sample")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Saving the audio sample")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    audio_data = b''.join(frames)
    return audio_data

audio_data = capture_audio()

encoded_audio = base64.b64encode(audio_data).decode('utf-8')

try:
    response = requests.post(shazam_url, headers=headers, data=encoded_audio)
    print(response.status_code)

    if response.status_code == 200:
        shazam_response = json.loads(response.content)
        title = shazam_response['track']['title']
        print("Recognized Song Title:", title)
    else:
        print("Song recognition failed.")

    with open("shazam_response.txt", "wb") as f:
        f.write(response.content)
except requests.exceptions.RequestException as e:
    print("Error making request:", e)
