

keymap = {}

"""
oct = 44100
for x in range(13):
    print oct + (x*(oct/12))

print "---"

oct = 22050
for x in range(13):
    print oct + (x*(oct/12))

middleoct = 44100
"""

notenames = {
    60: 'C-5',
    61: 'C#-5',
    62: 'D-5',
    63: 'D#-5',
    64: 'E-5',
    65: 'F-5',
    66: 'F#-5',
    67: 'G-5',
    68: 'G#-5',
    69: 'A-5',
    70: 'A#-5',
    71: 'B-5',
    72: 'C-6',
    73: 'C#-6',
    74: 'D-6',
    75: 'D#-6',
    76: 'E-6',
    48: 'C-4',
    49: 'C#-4',
    50: 'D-4',
    51: 'D#-4',
    52: 'E-4',
    53: 'F-4',
    54: 'F#-4',
    55: 'G-4',
    56: 'G#-4',
    57: 'A-4',
    58: 'A#-4',
    59: 'B-4'
}

    
    
    

# it note values mapped to keys
itkeymap = {
    'Q' : 60,   # C
    '2' : 61,   # C#
    'W' : 62,   # D
    '3' : 63,   # D#
    'E' : 64,   # E
    'R' : 65,   # F
    '5' : 66,   # F#
    'T' : 67,   # G
    '6' : 68,   # G#
    'Y' : 69,   # A
    '7' : 70,  # A#
    'U' : 71,  # B
    'I' : 72,   # C
    '9' : 73,   # C#
    'O' : 74,   # D
    '0' : 75,   # D#
    'P' : 76,   # E
    'Z' : 48,  # C
    'S' : 49,  # C#
    'X' : 50,  # D
    'D' : 51,  # D#
    'C' : 52,  # E
    'V' : 53,  # F
    'G' : 54,  # F#
    'B' : 55,  # G
    'H' : 56,  # G#
    'N' : 57,  # A
    'J' : 58, # A#
    'M' : 59, # B
    ',' : 60,   # C
    'L' : 61,   # C#
    '.' : 62,   # D
    ';' : 63,   # D#
    '/' : 64,   # E    
}    



def getitrate(absnote, c5speed=44100):
    noterate = c5speed * pow(2.0, (absnote-60)/12.0)
    return noterate

def itRateFromKey(char, c5speed=44100):
    note = itkeymap.get(char, 0)
    if note:
        rate = getitrate(note, c5speed)
        return rate
    else:
        return 0
    

#sampleratetoplay = tranpose * pow(2.0, (note-C-5note)/12)
def itnoterate(note, octave=0, c5speed=44100):
    fullnote = ((5+octave)*12)+note
    noterate = c5speed * pow(2.0, (fullnote-60)/12.0)
    return noterate

def noterate(note, octave=0):
    # note is 0..11
    # octave is relative to middle, where 44100 is the middle, C-5.  0 is 44100.

    if octave > 0:
        octrate = 44100
        for x in range(octave):
            octrate = octrate * 2
    elif octave < 0:
        octrate = 44100
        for x in range(abs(octave)):
            octrate = octrate / 2
    else:
        octrate = 44100
    noterate = octrate + (note * (octrate / 12))

    return noterate

def octrates(octave=0):
    rates = [noterate(x, octave) for x in range(12)]
    return rates


#for o in range(-3, 3):
#    print "octave", 5+o
#    print octrates(o)


def getkeymap(c5speed):
    keymap = {
        'Q' : itnoterate(0, 0, c5speed),   # C
        '2' : itnoterate(1, 0, c5speed),   # C#
        'W' : itnoterate(2, 0, c5speed),   # D
        '3' : itnoterate(3, 0, c5speed),   # D#
        'E' : itnoterate(4, 0, c5speed),   # E
        'R' : itnoterate(5, 0, c5speed),   # F
        '5' : itnoterate(6, 0, c5speed),   # F#
        'T' : itnoterate(7, 0, c5speed),   # G
        '6' : itnoterate(8, 0, c5speed),   # G#
        'Y' : itnoterate(9, 0, c5speed),   # A
        '7' : itnoterate(10, 0, c5speed),  # A#
        'U' : itnoterate(11, 0, c5speed),  # B
        'I' : itnoterate(0, 1, c5speed),   # C
        '9' : itnoterate(1, 1, c5speed),   # C#
        'O' : itnoterate(2, 1, c5speed),   # D
        '0' : itnoterate(3, 1, c5speed),   # D#
        'P' : itnoterate(4, 1, c5speed),   # E
        'Z' : itnoterate(0, -1, c5speed),  # C
        'S' : itnoterate(1, -1, c5speed),  # C#
        'X' : itnoterate(2, -1, c5speed),  # D
        'D' : itnoterate(3, -1, c5speed),  # D#
        'C' : itnoterate(4, -1, c5speed),  # E
        'V' : itnoterate(5, -1, c5speed),  # F
        'G' : itnoterate(6, -1, c5speed),  # F#
        'B' : itnoterate(7, -1, c5speed),  # G
        'H' : itnoterate(8, -1, c5speed),  # G#
        'N' : itnoterate(9, -1, c5speed),  # A
        'J' : itnoterate(10, -1, c5speed), # A#
        'M' : itnoterate(11, -1, c5speed), # B
        ',' : itnoterate(0, 0, c5speed),   # C
        'L' : itnoterate(1, 0, c5speed),   # C#
        '.' : itnoterate(2, 0, c5speed),   # D
        ';' : itnoterate(3, 0, c5speed),   # D#
        '/' : itnoterate(4, 0, c5speed),   # E    
    }    

    return keymap    


keymap = {
    'Q' : noterate(0, 0),   # C
    '2' : noterate(1, 0),   # C#
    'W' : noterate(2, 0),   # D
    '3' : noterate(3, 0),   # D#
    'E' : noterate(4, 0),   # E
    'R' : noterate(5, 0),   # F
    '5' : noterate(6, 0),   # F#
    'T' : noterate(7, 0),   # G
    '6' : noterate(8, 0),   # G#
    'Y' : noterate(9, 0),   # A
    '7' : noterate(10, 0),  # A#
    'U' : noterate(11, 0),  # B
    'I' : noterate(0, 1),   # C
    '9' : noterate(1, 1),   # C#
    'O' : noterate(2, 1),   # D
    '0' : noterate(3, 1),   # D#
    'P' : noterate(4, 1),   # E
    'Z' : noterate(0, -1),  # C
    'S' : noterate(1, -1),  # C#
    'X' : noterate(2, -1),  # D
    'D' : noterate(3, -1),  # D#
    'C' : noterate(4, -1),  # E
    'V' : noterate(5, -1),  # F
    'G' : noterate(6, -1),  # F#
    'B' : noterate(7, -1),  # G
    'H' : noterate(8, -1),  # G#
    'N' : noterate(9, -1),  # A
    'J' : noterate(10, -1), # A#
    'M' : noterate(11, -1), # B
    ',' : noterate(0, 0),   # C
    'L' : noterate(1, 0),   # C#
    '.' : noterate(2, 0),   # D
    ';' : noterate(3, 0),   # D#
    '/' : noterate(4, 0),   # E    
}    

