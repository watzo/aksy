
import string, random
import utilx

"""
Octave||                     MIDI Note Numbers
   #  ||
      || C   | C#  | D   | D#  | E   | F   | F#  | G   | G#  | A   | A#  | B
------------------------------------------------------------------------------
  -1  ||   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |   9 |  10 |  11
   0  ||  12 |  13 |  14 |  15 |  16 |  17 |  18 |  19 |  20 |  21 |  22 |  23
   1  ||  24 |  25 |  26 |  27 |  28 |  29 |  30 |  31 |  32 |  33 |  34 |  35
   2  ||  36 |  37 |  38 |  39 |  40 |  41 |  42 |  43 |  44 |  45 |  46 |  47
   3  ||  48 |  49 |  50 |  51 |  52 |  53 |  54 |  55 |  56 |  57 |  58 |  59
   4  ||  60 |  61 |  62 |  63 |  64 |  65 |  66 |  67 |  68 |  69 |  70 |  71
   5  ||  72 |  73 |  74 |  75 |  76 |  77 |  78 |  79 |  80 |  81 |  82 |  83
   6  ||  84 |  85 |  86 |  87 |  88 |  89 |  90 |  91 |  92 |  93 |  94 |  95
   7  ||  96 |  97 |  98 |  99 | 100 | 101 | 102 | 103 | 104 | 105 | 106 | 107
   8  || 108 | 109 | 110 | 111 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119
   9  || 120 | 121 | 122 | 123 | 124 | 125 | 126 | 127 | 

midi octaves: -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
"""

C = [0,12,24,36,48,60,72,84,96,108,120]
Cs = [1,13,25,37,49,61,73,85,97,109,121]
D = [2,14,26,38,50,62,74,86,98,110,122]
Ds = [3,15,27,39,51,63,75,87,99,111,123]
E = [4,16,28,40,52,64,76,88,100,112,124]
F = [5,17,29,41,53,65,77,89,101,113,125]
Fs = [6,18,30,42,54,66,78,90,102,114,126]
G = [7,19,31,43,55,67,79,91,103,115,127]
Gs = [8,20,32,44,56,68,80,92,104,116,116]
A = [9,21,33,45,57,69,81,93,105,117,117]
As = [10,22,34,46,58,70,82,94,106,118,118]
B = [11,23,35,47,59,71,83,95,107,119,119]

Cf = B
Df = Cs
Ef = Ds
Ff = E
Gf = Fs
Af = Gs
Bf = As

Cb = Cf
Db = Df
Eb = Ef
Fb = Ff
Gb = Gf
Ab = Af
Bb = Bf

Es = F
Bs = C

c = 0
cs = 1
d = 2
ds = 3
e = 4
f = 5
fs = 6
g = 7
gs = 8
a = 9
as = 10
b = 11

cb = b
db = cs
eb = ds
fb = e
gb = fs
ab = gs
bb = as
es = f
bs = c


notes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]

# major keys
keyC = [C[0], D[0], E[0], F[0], G[0], A[0], B[0]]
keyDb = [Db[0], Eb[0], F[0], Gb[0], Ab[0], Bb[0], C[0]]
keyD = [D[0], E[0], Fs[0], G[0], A[0], B[0], Cs[0]]
keyEb = [Eb[0], F[0], G[0], Ab[0], Bb[0], C[0], D[0]]
keyE = [E[0], Fs[0], Gs[0], A[0], B[0], Cs[0], Ds[0]]
keyF = [F[0], G[0], A[0], Bb[0], C[0], D[0], E[0]]
keyFs = [Fs[0], Gs[0], As[0], B[0], Cs[0], Ds[0], Es[0]]
keyG = [G[0], A[0], B[0], C[0], D[0], E[0], Fs[0]]
keyAb = [Ab[0], Bb[0], C[0], Db[0], Eb[0], F[0], G[0]]
keyA = [A[0], B[0], Cs[0], D[0], E[0], Fs[0], Gs[0]]
keyBb = [Bb[0], C[0], D[0], Eb[0], F[0], G[0], A[0]]
keyB = [B[0], Cs[0], Ds[0], E[0], Fs[0], Gs[0], As[0]]

keyCs = keyDb
keyDs = keyEb
keyEs = keyF
keyFs = keyFs
keyGs = keyAb
keyAs = keyBb
keyBs = keyC

keyCb = keyB
keyFb = keyE
keyGb = keyFs

notes = {
    'C' : C,
    'C#' : Cs,
    'D' : D,
    'D#': Ds,
    'E' : E,
    'E#' : Es,
    'F' : F,
    'F#' : F,
    'G' : G,
    'G#' : Gs,
    'A' : A,
    'A#' : As,
    'B' : B,
    'B#' : Bs,
    'Cb' : Cb,
    'Db' : Db,
    'Eb' : Eb,
    'Fb' : Fb,
    'Gb' : Gb,
    'Ab' : Ab,
    'Bb' : Bb
    }

key = {
    'C' : keyC,
    'C#' : keyCs,
    'D' : keyD,
    'D#': keyDs,
    'E' : keyE,
    'E#' : keyEs,
    'F' : keyF,
    'F#' : keyF,
    'G' : keyG,
    'G#' : keyGs,
    'A' : keyA,
    'A#' : keyAs,
    'B' : keyB,
    'B#' : keyBs,
    'Cb' : keyCb,
    'Db' : keyDb,
    'Eb' : keyEb,
    'Fb' : keyFb,
    'Gb' : keyGb,
    'Ab' : keyAb,
    'Bb' : keyBb
    }

noteDict = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9,
            'A#': 10, 'B': 11, 'B#': 12, 'E#': 5, 'C-': -1, 'D-': 1, 'E-': 3, 'F-': 4, 'G-': 5,
            'A-': 8, 'B-': 10}



def note(name, octave=0):
    return notes[string.upper(name)][octave]

n = note

def keynote(keyname, index):
    return key[keyname][index]

def o(notelist, octave):
    notelist = utilx.tolist(notelist)
    octval = octave*12
    return map(lambda x,o=octval: x+o, notelist)


octave = o

#print n('A#',3)

