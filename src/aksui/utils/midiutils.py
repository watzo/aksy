import modelutils

# list of mpc pad -> notes, left -> right = 1 -> 16
mpcpads = [
            37,36,42,82,40,38,46,44,48,47,45,43,49,55,51,53, # a
            54,69,81,80,65,66,76,77,56,62,63,64,73,74,71,39, # b
            52,57,58,59,60,61,67,68,70,72,75,78,79,35,41,50, # c
            83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98  # d
            ]

mpc_banks_gm = [
            49,55,51,53, 
            48,47,45,43,
            40,38,46,44,
            37,36,42,82,
            73,74,71,39, 
            65,66,76,77,
            56,62,63,64,
            54,69,81,80,
            79,35,41,50, 
            70,72,75,78,
            60,61,67,68,
            52,57,58,59,
            95,96,97,98, 
            91,92,93,94,
            87,88,89,90,
            83,84,85,86,
            ]
mpc_banks_chromatic = [
            48,49,50,51, 
            44,45,46,47,
            40,41,42,43,
            36,37,38,39,
            64,65,66,67,
            60,61,62,63,
            56,57,58,59,
            52,53,54,55,
            80,81,82,83,
            76,77,78,79,
            72,73,74,75,
            68,69,70,71,
            96,97,98,99,
            92,93,94,95,
            88,89,90,91,
            84,85,86,87,
            ]

notes = ['C','C#','D','Eb','E','F','F#','G','G#','A','Bb','B']
octaves = [i for i in range(-2, 9)]
octaves_snap = [i for i in range(0, 127, 12)]
midinotes = { }

i = 0

for oct in octaves:
    for note in notes:
        if i > 127:
            break
        if oct >= 0 and len(note) == 1:
            n = note + ' ' + str(oct)
        else:
            n = note + str(oct)
        midinotes[i] = n
        i = i + 1        

mpcpadsmodel = modelutils.get_model_from_list(mpcpads)
midinotesmodel = modelutils.get_model_from_list(midinotes)

# views for drum editor
note_orders = {
    "chromatic" : midinotes,
    "mpc_banks_gm": mpc_banks_gm,
    "mpc_banks_chromatic" : mpc_banks_chromatic
    }

# general midi 1 drum map
gm1drumsmap = {
    35:"Acoustic Bass Drum",
    36:"Bass Drum 1",
    37:"Side Stick",
    38:"Acoustic Snare",
    39:"Hand Clap",
    40:"Electric Snare",
    41:"Low Floor Tom",
    42:"Closed Hi Hat",
    43:"High Floor Tom",
    44:"Pedal Hi-Hat",
    45:"Low Tom",
    46:"Open Hi-Hat",
    47:"Low-Mid Tom",
    48:"Hi-Mid Tom",
    49:"Crash Cymbal 1",
    50:"High Tom",
    51:"Ride Cymbal 1",
    52:"Chinese Cymbal",
    53:"Ride Bell",
    54:"Tambourine",
    55:"Splash Cymbal",
    56:"Cowbell",
    57:"Crash Cymbal 2",
    58:"Vibraslap",
    59:"Ride Cymbal 2",
    60:"Hi Bongo",
    61:"Low Bongo",
    62:"Mute Hi Conga",
    63:"Open Hi Conga",
    64:"Low Conga",
    65:"High Timbale",
    66:"Low Timbale",
    67:"High Agogo",
    68:"Low Agogo",
    69:"Cabasa",
    70:"Maracas",
    71:"Short Whistle",
    72:"Long Whistle",
    73:"Short Guiro",
    74:"Long Guiro",
    75:"Claves",
    76:"Hi Wood Block",
    77:"Low Wood Block",
    78:"Mute Cuica",
    79:"Open Cuica",
    80:"Mute Triangle",
    81:"Open Triangle"}

sampler_lists = {
    "filter" : ["Off", "2-Pole LP","2-Pole LP+","4-Pole LP","4-Pole LP+","6-Pole LP","2-Pole BP","2-Pole BP+","4-Pole BP","4-Pole BP+","6-Pole BP","1-Pole HP", "1-Pole HP+", "2-Pole HP", "2-Pole HP+", "6-Pole HP", "LO&lt;&gt;HI", "LO&lt;&gt;BAND", "BAND&lt;&gt;HI", "Notch 1", "Notch 2", "Notch 3", "Wide Notch", "Bi-Notch", "Peak 1", "Peak 2", "Peak 3", "Wide Peak", "Bi-Peak", "Phaser 1", "Phaser 2", "Bi-Phase", "Voweliser", "Triple"],
    "output" : ["L-R", "1-2", "3-4", "5-6", "7-8", "L", "R", "1", "2", "3", "4", "5", "6", "7", "8"],
    "midi_channel" : ["1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A", "11A", "12A", "13A", "14A", "15A", "16A", "1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "10B", "11B", "12B", "13B", "14B", "15B", "16B"],
    "filter_attenuation" : ["0db", "6db","12db","18db","24db","30db"],
    "fx_override" : ["Off", "A","B","C","D","AB","CD","Multi"],
    "zone_xfade" : ["Off", "Velocity", "Real-Time"],
    "zone_xfade_type" : ["Lin", "Exp", "Log"],
    "keygroup_edit_mode" : ["Single", "All","Add"],
    "keyboard_track" : ["Off", "On"],
    "playback" : ["1 Shot","LIR","LUR","LIR-&gt;Rt","Retrig","As Sample"],
    "playback_b" : ["Sample","1 Shot","No Loop","Loop"],
    "play_trigger" : ["Note On", "Note Off"],
    "glissando_mode" : ["Portamento", "Glissando"],
    "portamento_mode" : ["Time", "Rate"],
    "legato" : ["Off", "Pitch", "Loop"],
    "aftertouch_mode" : ["Channel", "Poly"],
    "pitchbend_mode" : ["Normal", "Held"],
    "program_type" : ["Keygroup", "Drum"],
    "keygroup_xfade_type" : ["Exp", "Log"],
    "reassignment_method" : ["Quietest", "Oldest"],
    "lfo_waves" : ["TRIANGLE", "SINE", "SQUARE", "SAW UP", "SAW DOWN", "RANDOM"],
    "lfo_retrigger" : ["Off", "On"],
    "lfo_sync" : ["Off", "On"],
    "lfo_midi_sync" : ["Off", "On"],
    "record_trigger_src" : ["OFF", "AUDIO", "MIDI"],
    "record_bit_depth" : ["16-Bit", "24-Bit"],
    "record_input" : ["ANALOGUE", "DIGITAL", "MAIN OUT", "ADAT 1/2", "ADAT 3/4", "ADAT 5/6", "ADAT 7/8"],
    "record_mode" : ["STEREO", "MONO L", "MONO R", "MONO L+R MIX"],
}
