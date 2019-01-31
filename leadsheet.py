import abjad

class Leadsheet():

    def __init__(self, title = 'DoJoy VMPT leadsheet generated chord', bpm = 60, measureCount = 4, measureDuration = 4, quantize = 4):
        self.title = title
        self.bpm = bpm
        self.measureCount = measureCount
        self.measureDuration = measureDuration
        self.quantize = 4
        self.chords = list()
        self.startSheet()

    def startSheet(self):
        self.sheet      = '\\header {  title = \"' + self.title + '\"}\n'

        self.sheet += '<< \\new ChordNames { \\set chordChanges = ##t \\chordmode { \n'

    def writeSheet(self):
        self.startSheet()

        scoreDuration = 0

        for i in range(0,len(self.chords)):

            duration = self.getQuantifizedDuration(i,  scoreDuration)
            if duration < 1:
                #todojoy fix bug
                duration = 1
                #raise ValueError('A very specific bad thing happened.')


            # TODO BUG abjac doesnt work with durations greater one MEASURE 11/2
            dur = abjad.Duration(duration,  self.quantize)

            while duration > self.quantize:
                tmpdur = abjad.Duration(self.quantize, self.quantize)
                chord = chordinoChordToLy(self.chords[i][0], tmpdur.lilypond_duration_string)
                self.sheet += ' ' + chord
                duration = duration - self.quantize
                dur = abjad.Duration(duration, self.quantize)
                scoreDuration += int(duration)
            # DUPLICATE CODE ABOVE extract add chord
            chord = chordinoChordToLy(self.chords[i][0], dur.lilypond_duration_string)
            self.sheet += ' ' + chord

            scoreDuration += int(duration)

        self.sheet += '\n }}  \n\\relative c'' { \n'

        for s in range(0, scoreDuration):
            self.sheet += ' r' + str(self.quantize)

        self.sheet += '\n  }>>'

    def getLyDuration(self, position):
        if position == len(self.chords) -1:
            return self.quantize

        time = self.chords[position + 1][1] - self.chords[position][1]

        return self.getLyDurationFromTime(time)

    def getLyDurationFromTime(self, time):

        #quantizematrix ... allowed values

        return round(60. * self.measureDuration / self.bpm / time)

    def getQuantifizedDuration(self, position,  lyScoreDuration):
        if position == len(self.chords) - 1:
            return 1

        nextTime = self.chords[position + 1][1]
        
        nextLyPosition = self.getQuantifizedDurationFromTime(nextTime)
        return nextLyPosition - lyScoreDuration
        

        #rTime = self.chords[position + 1][1] - self.chords[position][1]
        #time = rTime.sec + float(rTime.nsec / 1000000000.)

        #return self.getQuantifizedDurationFromTime(time)

    def getQuantifizedDurationFromTime(self, time):
        # title is wrong . needs quantize.....
        return int(round((self.quantize/4.) *  time * self.bpm / 60.))

    def addChord(self, chord, timestamp):
        self.chords.append([chord,timestamp])

    def printSheet(self):
        self.writeSheet()
        print (self.sheet)
        
    def getSheet(self):
        self.writeSheet()
        return self.sheet

notes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
notesDistance = [2,1,2,2,1,2,2]

notesDistanceMajor = [2,2,1,2,2,2,1]
notesDistanceMinor = notesDistance


def getScale(strTonic, isMinor=False):

    accModifier = 0
    if len(strTonic) != 1:
        if strTonic[1:] == 'is':
            accModifier = -1
        elif strTonic[1:] == 'es':
            accModifier = +1

    tonicIndex = notes.index(strTonic[0])

    res = []

    for i in range(0,7):
        noteIndex = (i+tonicIndex)%7
        note = notes[noteIndex]

        dist = accModifier
        correctDistance = 0
        for d in range(0,i):
            dist += notesDistance[(tonicIndex + d)%7]
            if isMinor:
                correctDistance += notesDistanceMinor[d]
            else:
                correctDistance += notesDistanceMajor[d]

        if correctDistance - dist == 1:
            note += 'is'
        elif correctDistance - dist == -1:
            note += 'es'

        res.append(note)

    return res


def calcBass(strBass, strTonic, isMinor=False):
    bassModifier = ''

    if len(strBass) == 2:
        bassIndex = int(strBass[1]) - 1

        if strBass[0] == 'b':
            bassModifier = 'es'
        elif strBass[0] == '#':
            bassModifier = 'is'
    else:
        bassIndex = int(strBass[0]) - 1

    bass = getScale(strTonic, isMinor) [bassIndex]

    if len(bass) > 1 and bassModifier != '':
        if bass[1:] == 'is' and bassModifier == 'es' or bass[1:] == 'es' and bassModifier == 'is':
            bass = bass[0]
        else:
            bass += bassModifier

    return bass

def chordinoChordToLy(chord, duration):
    #NoChord symbol
    if chord == 'N':
        return 'r' + str(duration)

    if len(chord) < 2:
        return chord.lower() + str(duration)

    chord = chord.lower()

    #BASE + DURATION + ifmodifier : modifier + ifbass /bass

    base = chord[0]

    position = 1

    if chord[1] == 'b':
        base += 'es'
        position += 1
    elif chord[1] == '#':
        base += 'is'
        position += 1

    basspos = chord.find('/')

    posendmod = basspos if basspos != -1 else len(chord)

    modifier = chord[position:posendmod]
    if modifier != '' and modifier[0] != ':':
        modifier = ':' + modifier

    modifier = modifier.replace('hdim7', '7.5-')

    bass = ''
    if basspos != -1:
        bass = chord[basspos + 1:]
        bass = calcBass(bass, base, chord[1] == 'm')

    if bass != '':
        bass = '/' + bass

    return '{0}{1}{2}{3}'.format(base, str(duration), modifier, bass)

def chordinoChordToLyOld(chord, duration):

    #refactor:::: statt immer einzubasteln, aus bestandteilen zusammensetzen!!!!

    #NoChord symbol
    if chord == 'N':
        return 'r' + str(duration)

    resChord = chord.lower()

    if len(chord) < 2:
        return resChord + str(duration)

    #accidentials
    #Harte b #
    #ly es is

    startSplit = 1
    if chord[1] == 'b':
        resChord = resChord[0] + 'es' + resChord[2:]
        startSplit += 2
    elif chord[1] == '#':
        resChord = resChord[0] + 'is' + resChord[2:]
        startSplit += 2

    #endSplit = startSplit if resChord.find(':') == -1 else startSplit + 1

    resChord = resChord[:startSplit] + str(duration)

    resChord += chord[startSplit:]

    #if chord.find(':') != -1:
    #resChord += ':'
    #resChord += resChord[endSplit:]

    basspos = chord.find('/')
    if basspos != -1:
        resChord = resChord[:basspos + 2]
        #resChord += '/'
        resChord += calcBass(chord[basspos + 1:], resChord[0], chord[1] == 'm')

    resChord = resChord.replace('hdim7', '7.5-')
    return resChord
