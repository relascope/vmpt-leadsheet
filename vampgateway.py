import sys
import vamp
import librosa


class VampGateway():

    def __init__(self):
        self.loadedFile = ''

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
        chorddata = vamp.collect(data, rate, "nnls-chroma:chordino", "simplechord", {'useNNLS':1, 'rollon':0, 'tuningmode':0, 'whitening':1,
        's':0.699999988, 'boostn':0.100000001,  'usehartesyntax':1.0})

        return chorddata['list']

def main(argv):
    filename = sys.argv[1]

    gw = VampGateway()

    bpm = gw.getBpmFromFile(filename)
    chords = gw.getChordsFromFile(filename)

    print ("BPM: " + bpm)
    print (chords)

if __name__ == "__main__":
    main(sys.argv)
