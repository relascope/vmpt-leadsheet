#!/usr/bin/env python3

import leadsheet
import os
import sys
import tkinter
import vampgateway

def printUsage(argv):
    print ("Usage: " + argv[0] + " InputAudioFile + [OutputLilypondFile]")

def main(argv):
    outFile = ""

    if len(argv) == 2 and argv[1] == "--help":
        printUsage(argv)
        exit(0)

    if len(argv) < 2 or len(argv) > 3:

#DEBUG HACK 
#        filename = "/home/dojoy/dev/vmpt-leadsheet/Testfile.wav"    
#        outFile = "/home/dojoy/dev/vmpt-leadsheet/Testfile.ly"    
#END DEBUG HACK
# 
        #assume GUI
        rootWindow = tkinter.Tk()

        inputLabel = tkinter.Label(rootWindow, text="Input Audio File: ")
        inputLabel.pack()
        inputEntry = tkinter.Entry(rootWindow)
        inputEntry.pack()
        outputLabel = tkinter.Label(rootWindow, text="Output Score File")
        outputLabel.pack()
        outputEntry = tkinter.Entry(rootWindow)
        outputEntry.pack()

        okButton = tkinter.Button(rootWindow, text="Convert", command=rootWindow.quit)
        okButton.pack()

        infoLabel = tkinter.Label(rootWindow, text="There is also a commandline Version of the Program. For information start with --help. ")
        infoLabel.pack()

        rootWindow.protocol("WM_DELETE_WINDOW", func=exit)

        rootWindow.mainloop()

        filename = inputEntry.get()
        outFile = outputEntry.get()
    else: 
        filename = argv[1]

    if len(argv) == 3:
        outFile = argv[2]

    vgw = vampgateway.VampGateway()

    chords = vgw.getChordsFromFile(filename)
    bpm = vgw.getBpmFromFile(filename)

    title = os.path.basename(os.path.splitext(filename)[0])

    ls = leadsheet.Leadsheet(title, bpm)

    for c in chords:
        rTime = c['timestamp']
        timestamp = rTime.sec + float(rTime.nsec / 1000000000.)

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
