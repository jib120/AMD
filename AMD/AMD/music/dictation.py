#!/usr/bin/python3
from subprocess import Popen, PIPE
import sys
import math
from music21 import *



ROOT_DIR="/home/kwlee/AMD/AMD/"

middleC = 60  # C4 midi-like notes notation
note_table = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def duration_roundup(d1, d2):
    duration = float(d2) - float(d1)
    return round(duration * 10)/10.0


def get_notes(pitch):
    diff = pitch - middleC
    note = note_table[diff % 12] + str(4 + (int(diff / 12)))
    return note

def convert(filename):

    print(filename)

    us = environment.UserSettings()
    us['lilypondPath'] = "/usr/bin/lilypond"
    print(us['lilypondPath'] )

    '''
    noteC = note.Note("C#4", type="half")
    noteD = note.Note("D4", type="quarter")
    noteE = note.Note("E4", type="quarter")
    noteF = note.Note("F4", type="half")
    '''
    # print(tsThreeFour.numerator, '/',  tsThreeFour.denominator)

    stream1 = stream.Stream()
    tsThreeFour = meter.TimeSignature('4/4')
    stream1.append(tsThreeFour)
    #for thisThing in [tsThreeFour, noteC, noteD, noteE, noteF]:
    #    stream1.append(thisThing)


    process = Popen(["aubionotes", "-v", ROOT_DIR+filename], stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    #print(err)
    prevDur = 0
    for l in err.splitlines():
        line = l.split()
        s = line[0]
        if not is_number(s):
            continue

        if len(line) != 1 and len(line) != 3:
            continue #TODO: rest

        if len(line) == 1:
            dur  = duration_roundup(prevDur, line[0])
            no = note.Rest(quarterLength=dur)
        else:
            dur = duration_roundup(line[1], line[2])
            prevDur = float(line[2])
            no = note.Note(get_notes(int(float(line[0]))), quarterLength=dur)

        if dur > 24:
            times = int(dur / 24)

            for i in range(0, times):
                if len(line) == 1:
                    longa = note.Rest(quarterLength=24)
                else:
                    longa = note.Note(get_notes(int(float(line[0]))), quarterLength=24)
                stream1.append(longa)

            remain = dur % 24
            no.quarterLength = remain

        stream1.append(no)

    conv = converter.subConverters.ConverterLilypond()
    conv.write(stream1, fmt='lilypond', fp=ROOT_DIR+'media/twice', subformats=['png'])


