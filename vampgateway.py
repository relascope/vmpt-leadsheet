import sys
import vamp
import librosa


class VampGateway():

    def __init__(self):
        self.loadedFile = ''
        self.data = None
        self.rate = None

    def getBpmFromFile(self,  filename):
        if self.loadedFile != filename:
            self.loadedFile = filename
            self.data, self.rate = librosa.load(filename, sr=None)

        return self.getBpm(self.data, self.rate)

    def getBpm(self,  data, rate):
        tempo = vamp.collect(data, rate, "vamp-example-plugins:fixedtempo", "tempo")

        return tempo['list'][0]['values'][0]

    def getChordsFromFile(self,  filename):
        if self.loadedFile != filename:
            self.loadedFile = filename
            self.data, self.rate = librosa.load(filename, sr=None)

        return self.getChords(self.data, self.rate)

    def getChords(self,  data, rate):
        # TO Watch: vamp doesn't find specific plugin simplechord, hopefully it will stay the default plugin in chordino
        chorddata = vamp.collect(data=data, sample_rate=rate, plugin_key="nnls-chroma:chordino", parameters = {'useNNLS':1, 'usehartesyntax':1.0})

        return chorddata['list']