import unittest

import re

from leadsheet import *

class TestLeadsheet(unittest.TestCase):
    
    def getChordsFromLyString(self,  sheet):
        cpos = sheet.find('chordmode')
        cstart  = sheet.find('{',  cpos) + 1
        cend = sheet.find('}',  cstart)        
        return sheet[cstart:cend].split()
    
    def getDurations(self,  sheet):
        chords = self.getChordsFromLyString(sheet)

        durations = list()
        
        for c in chords:
            durs = re.findall(r'\d+',  c)
            durations.append(int(durs[0]))

        return durations
    
    def testScoreDurationQuarter(self):
        
        ls = Leadsheet()
        
        ls.addChord('a',  0.)
        ls.addChord('b',  1.)
        ls.addChord('c',  2.)
        ls.addChord('d',  3.)
                
        durations = self.getDurations(ls.getSheet())
        
        for d in durations:
            self.assertEqual(4,  d)
            
    def testScoreDurations(self):
        
        ls = Leadsheet()
        
        ls.addChord('a',  0.)
        ls.addChord('b',  1.5)
        ls.addChord('c',  4.)
        ls.addChord('d',  6.)
                
        durations = self.getDurations(ls.getSheet())
        
        print ls.getSheet()
        
        self.assertEqual(2,  durations[0])
        self.assertEqual(2,  durations[1])
        self.assertEqual(2,  durations[2])

    def testLyDurationBpm(self):

        #time in seconds, expected lyDuration
        durations = [
        [1,2],
        [2,1],
        # [4,1], # TODO
        [0.5,4],
        [0.25,8],
        #[8,0.5], # TODO

        [1.00006, 2],
        [1.98, 1],

        [2.4, 1],
        ]

        ls = Leadsheet('', 120)

        for d in durations:
            lyDuration = ls.getLyDurationFromTime(d[0])
            self.assertEqual(lyDuration, d[1], 'Input: {0} should be {1} but was {2}.'.format(d[0], d[1], lyDuration))

        #time in seconds, expected lyDuration
        durations = [
        [1,8],
        [2,4],
        [4,2],
        [0.5,16],
        [0.25,32],
        #[8,0.5], # TODO

        [1.00006, 8],
        [1.98, 4],

        [2.4, 3],
        ]

        ls = Leadsheet('', 30)

        for d in durations:
            lyDuration = ls.getLyDurationFromTime(d[0])
            self.assertEqual(lyDuration, d[1], 'Input: {0} should be {1} but was {2}.'.format(d[0], d[1], lyDuration))

    def testLyDurationStandard(self):

        #time in seconds, expected lyDuration
        durations = [
        [1,4],
        [2,2],
        [4,1],
        [0.5,8],
        [0.25,16],
        #[8,0.5], # TODO

        [1.00006, 4],
        [1.98, 2],

        [2.4, 2],
        ]

        ls = Leadsheet()

        for d in durations:
            lyDuration = ls.getLyDurationFromTime(d[0])
            self.assertEqual(lyDuration, d[1], 'Input: {0} should be {1} but was {2}.'.format(d[0], d[1], lyDuration))

    def testChords(self):

        #inputChord, inputDuration, [expectedValues...]
        chords = [
        ['C/5', 4, ['c4/g']],
        ['E', 4, ['e4']],
        ['Am', 4, ['a4:m']],
        ['Bb', 4, ['bes4','bes4:']],
        ['A:7/3', 8, ['a8:7/cis']],
        ['A:7/#3', 2, ['a2:7/cisis']],
        ['Am7', 4, ['a4:m7']],
        ['E:hdim7/b7',4, ['e4:7.5-/d']],
        ['C', 16, ['c16']],
        ['E', 128, ['e128']],
        ['Fb:m', 128, ['fes128:m']],
        ]

        for c in chords:
            lyChord = chordinoChordToLy(c[0], c[1])

            self.assertIn(lyChord, c[2], 'Input ' + c[0] + ' duration ' + str(c[1]) + ' expected on of' + str(c[2]) + ' but was ' + lyChord)

if __name__ == '__main__':
    unittest.main()
