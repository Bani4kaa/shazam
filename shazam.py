import requests
import pyaudio
import io
import base64
import json
import tkinter as tk
from PIL import Image, ImageTk
import sounddevice as sd

shazam_url = 'https://shazam.p.rapidapi.com/songs/detect'
headers = {
    'content-type': 'text/plain',
    'X-RapidAPI-Key': 'ur api key here',
    'X-RapidAPI-Host': 'shazam.p.rapidapi.com'
}


def capture_audio():
    pulse()
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

def recognize_song():
    pulse()
    audio_data = capture_audio()
    encoded_audio = base64.b64encode(audio_data).decode('utf-8')

    try:
        response = requests.post(shazam_url, headers=headers, data=encoded_audio)

        if response.status_code == 200:
            shazam_response = json.loads(response.content)
            title = shazam_response['track']['title']
            result_label.config(text=f"Recognized Song Title: {title}")
        else:
            result_label.config(text="Failed to recognize song.")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error making request: {e}")
    stop_pulse()
def pulse():
    global pulsing
    pulsing = True
    if pulsing:
        canvas.itemconfig(circle, fill="red")
        root.after(500, lambda: canvas.itemconfig(circle, fill="green"))
        root.after(1000, pulse)

def stop_pulse():
    global pulsing
    pulsing = False
    canvas.itemconfig(circle, fill="green")

root = tk.Tk()
root.title("Shazam Song Recognition")

icon_image = Image.open("favicon.ico")
icon_image = icon_image.resize((16, 16), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon_image)

root.iconphoto(True, icon)

info_label = tk.Label(root, text="This is the Shazam Song Recognition Program")
info_label.grid(row=0, column=0, padx=10, pady=10)

canvas = tk.Canvas(root, width=100, height=100)
canvas.grid(row=1, column=0, padx=20, pady=20)

circle = canvas.create_oval(10, 10, 90, 90, outline="black", fill="green")

canvas.tag_bind(circle, '<ButtonPress-1>', lambda x: pulse())
canvas.tag_bind(circle, '<ButtonRelease-1>', lambda x: recognize_song())

result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, padx=20)

root.mainloop()
