# shazam
Shazam but on pc ran by python
Detect songs from raw sound data. The raw sound data must be 44100Hz, 1 channel (Mono), signed 16 bit PCM little endian. Other types of media are NOT supported, such as : mp3, wav, etc… or need to be converted to uncompressed raw data. If the result is empty, your request data must be in wrong format in most case. Encoded base64 string of byte[] that generated from raw data less than 500KB (3-5 seconds sample are good enough for detection) will be sent via body as plain text

Requirements: 


requests
pyaudio
io
base64
json

rapidapi api service ( there is free tier )



api service --> https://rapidapi.com/apidojo/api/shazam

shazam.com --> https://www.shazam.com/apps
