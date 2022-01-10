
import sounddevice
import playback
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

try:
    sd = sounddevice.OutputStream(device=config.AUDIO_DEVICE_ID, blocksize=512, samplerate=44100, channels=2, dtype='int16', callback=playback.AudioCallback)
    sd.start()
    print('Opened audio device #%i' % config.AUDIO_DEVICE_ID)
except:
    print('Invalid audio device #%i' % config.AUDIO_DEVICE_ID)
    exit(1)