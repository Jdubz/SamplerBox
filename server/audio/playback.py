import numpy
from audio import samplerbox_audio
from samples import waveread
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

playingsounds = []
globalvolume = 10 ** (-12.0/20)  # -12dB default global volume

FADEOUTLENGTH = 30000
FADEOUT = numpy.linspace(1., 0., FADEOUTLENGTH)            # by default, float64
FADEOUT = numpy.power(FADEOUT, 6)
FADEOUT = numpy.append(FADEOUT, numpy.zeros(FADEOUTLENGTH, numpy.float32)).astype(numpy.float32)
SPEED = numpy.power(2, numpy.arange(0.0, 84.0)/12).astype(numpy.float32)

class PlayingSound:

    def __init__(self, sound, note):
        self.sound = sound
        self.pos = 0
        self.fadeoutpos = 0
        self.isfadeout = False
        self.note = note

    def fadeout(self, i):
        self.isfadeout = True

    def stop(self):
        try:
            playingsounds.remove(self)
        except:
            pass


class Sound:

    def __init__(self, filename, midinote, velocity):
        wf = waveread(filename)
        self.fname = filename
        self.midinote = midinote
        self.velocity = velocity
        if wf.getloops():
            self.loop = wf.getloops()[0][0]
            self.nframes = wf.getloops()[0][1] + 2
        else:
            self.loop = -1
            self.nframes = wf.getnframes()

        self.data = self.frames2array(wf.readframes(self.nframes), wf.getsampwidth(), wf.getnchannels())

        wf.close()

    def play(self, note):
        snd = PlayingSound(self, note)
        playingsounds.append(snd)
        return snd

    def frames2array(self, data, sampwidth, numchan):
        if sampwidth == 2:
            npdata = numpy.fromstring(data, dtype=numpy.int16)
        elif sampwidth == 3:
            npdata = samplerbox_audio.binary24_to_int16(data, len(data)/3)
        if numchan == 1:
            npdata = numpy.repeat(npdata, 2)
        return npdata

def AudioCallback(outdata, frame_count, time_info, status):
    global playingsounds
    rmlist = []
    playingsounds = playingsounds[-config.MAX_POLYPHONY:]
    b = samplerbox_audio.mixaudiobuffers(playingsounds, rmlist, frame_count, FADEOUT, FADEOUTLENGTH, SPEED)
    for e in rmlist:
        try:
            playingsounds.remove(e)
        except:
            pass
    b *= globalvolume
    outdata[:] = b.reshape(outdata.shape)