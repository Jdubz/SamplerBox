import wave
import struct
from chunk import Chunk

class waveread(wave.Wave_read):

    def initfp(self, file):
        self._convert = None
        self._soundpos = 0
        self._cue = []
        self._loops = []
        self._ieee = False
        self._file = Chunk(file, bigendian=0)
        if self._file.getname() != 'RIFF':
            raise RuntimeError('file does not start with RIFF id')
        if self._file.read(4) != 'WAVE':
            raise RuntimeError('not a WAVE file')
        self._fmt_chunk_read = 0
        self._data_chunk = None
        while 1:
            self._data_seek_needed = 1
            try:
                chunk = Chunk(self._file, bigendian=0)
            except EOFError:
                break
            chunkname = chunk.getname()
            if chunkname == 'fmt ':
                self._read_fmt_chunk(chunk)
                self._fmt_chunk_read = 1
            elif chunkname == 'data':
                if not self._fmt_chunk_read:
                    raise RuntimeError('data chunk before fmt chunk')
                self._data_chunk = chunk
                self._nframes = chunk.chunksize // self._framesize
                self._data_seek_needed = 0
            elif chunkname == 'cue ':
                numcue = struct.unpack('<i', chunk.read(4))[0]
                for i in range(numcue):
                    id, position, datachunkid, chunkstart, blockstart, sampleoffset = struct.unpack('<iiiiii', chunk.read(24))
                    self._cue.append(sampleoffset)
            elif chunkname == 'smpl':
                manuf, prod, sampleperiod, midiunitynote, midipitchfraction, smptefmt, smpteoffs, numsampleloops, samplerdata = struct.unpack(
                    '<iiiiiiiii', chunk.read(36))
                for i in range(numsampleloops):
                    cuepointid, type, start, end, fraction, playcount = struct.unpack('<iiiiii', chunk.read(24))
                    self._loops.append([start, end])
            chunk.skip()
        if not self._fmt_chunk_read or not self._data_chunk:
            raise RuntimeError('fmt chunk and/or data chunk missing')

    def getmarkers(self):
        return self._cue

    def getloops(self):
        return self._loops

