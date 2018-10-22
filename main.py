import leadsheet
import vampgateway
import sys
import os

def printUsage(argv):
    print ("Usage: " + argv[0] + " InputAudioFile + [OutputLilypondFile]")

def main(argv):
    if len(argv) < 2 or len(argv) > 2:
        printUsage(argv)
        exit(0)

    filename = argv[1]

    if len(argv) == 3:
        outFile = argv[2]
    else:
        outFile = ""

    vgw = vampgateway.VampGateway()

    chords = vgw.getChordsFromFile(filename)
    bpm = vgw.getBpmFromFile(filename)

    title = os.path.basename(os.path.splitext(filename)[0])

    ls = leadsheet.Leadsheet(title, bpm)

    for c in chords:
        rTime = c['timestamp']
        timestamp =         time = rTime.sec + float(rTime.nsec / 1000000000.)

        ls.addChord(c['label'], timestamp)

    if outFile == "":
        ls.printSheet()
    else:
        sheet = ls.getSheet()
        file = open(outFile,  'w')
        file.write(sheet)
        file.close()

if __name__ == "__main__":
    main(sys.argv)
