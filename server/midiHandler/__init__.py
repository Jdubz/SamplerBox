import threading
import rtmidi_python as rtmidi
import time

class Midi:
    def __init__(self, config, samples, globaltranspose, preset, loadSamples):
        self.config = config
        self.playingnotes = {}
        self.sustain = False
        self.sustainplayingnotes = []
        self.samples = samples
        self.globaltranspose = globaltranspose
        self.preset = preset
        self.loadSamples = loadSamples

    def setPreset(self, preset):
        self.preset = preset

    def setSamples(self, samples):
        self.samples = samples

    def setTranspose(self, transpose):
        self.globaltranspose = transpose

    def midiCallback(self, message, time_stamp):
        global preset
        messagetype = message[0] >> 4
        messagechannel = (message[0] & 15) + 1
        note = message[1] if len(message) > 1 else None
        midinote = note
        velocity = message[2] if len(message) > 2 else None

        if messagetype == 9 and velocity == 0:
            messagetype = 8

        if messagetype == 9:    # Note on
            midinote += self.globaltranspose
            try:
                self.playingnotes.setdefault(midinote, []).append(self.samples[midinote, velocity].play(midinote))
            except:
                pass

        elif messagetype == 8:  # Note off
            midinote += self.globaltranspose
            if midinote in self.playingnotes:
                for n in self.playingnotes[midinote]:
                    if self.sustain:
                        self.sustainplayingnotes.append(n)
                    else:
                        n.fadeout(50)
                self.playingnotes[midinote] = []

        elif messagetype == 12:  # Program change
            print('Program change ' + str(note))
            self.preset = note
            self.loadSamples()

        elif (messagetype == 11) and (note == 64) and (velocity < 64):  # sustain pedal off
            for n in self.sustainplayingnotes:
                n.fadeout(50)
            self.sustainplayingnotes = []
            self.sustain = False

        elif (messagetype == 11) and (note == 64) and (velocity >= 64):  # sustain pedal on
            self.sustain = True
