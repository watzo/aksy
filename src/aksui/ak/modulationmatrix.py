class ModulationMatrix:
    # should be a total of 36 (0 based) * marks sample + hold mods
    sources      = ['NONE','MODWHEEL','BEND UP','BEND DOWN',
                    'AFTERTOUCH','VELOCITY','BIPOLAR VELOCITY','OFF VELOCITY',
                    'KEYBOARD','LFO1','LFO2','AMP ENV',
                    'FILTER ENV','AUX ENV','MIDI CTRL','Q-LINK 1',
                    'Q-LINK 2','Q-LINK 3','Q-LINK 4','Q-LINK 5',
                    'Q-LINK 6','Q-LINK 7','Q-LINK 8','*MODWHEEL',
                    '*BEND UP','*BEND DOWN','*Q-LINK 1','*Q-LINK 2',
                    '*Q-LINK 3','*Q-LINK 4','*Q-LINK 5','*Q-LINK 6',
                    '*Q-LINK 7','*Q-LINK 8','*LFO1','*LFO2','*MIDI CTRL']

    # should be a total of 52 (0 based), qlink adds 4 'EXT' options
    destinations = ['NONE',           'AMPLITUDE',    'PAN',            'PITCH',
                    'LFO1 RATE',      'LFO1 DEPTH',   'LFO1 DELAY',     'LFO1 PHASE',
                    'LFO1 OFFSET',    'LFO2 RATE',    'LFO2 DEPTH',     'LFO2 DELAY',
                    'LFO2 PHASE',     'LFO2 OFFSET',  'CUTOFF',  'RESONANCE',
                    'TR 1 CUTOFF',    'TR 1 RES',     'TR 2 CUTOFF',    'TR 2 RES',
                    'TR 3 CUTOFF',    'TR 3 RES',     'AMP ENV ATTACK', 'AMP ENV DECAY',
                    'AMP ENV RELEASE','FILT ENV R1',  'FILT ENV R2',    'FILT ENV R4',
                    'AUX ENV R1',     'AUX ENV R2',   'AUX ENV R4',     'ZONE CROSSFADE',
                    'ZONE 1 LEVEL',   'ZONE 1 PAN',   'ZONE 1 PITCH',   'ZONE 1 START', 'ZONE 1 FILTER'
                    'ZONE 2 LEVEL',   'ZONE 2 PAN',   'ZONE 2 PITCH',   'ZONE 2 START', 'ZONE 2 FILTER'
                    'ZONE 3 LEVEL',   'ZONE 3 PAN',   'ZONE 3 PITCH',   'ZONE 3 START', 'ZONE 3 FILTER'
                    'ZONE 4 LEVEL',   'ZONE 4 PAN',   'ZONE 4 PITCH',   'ZONE 4 START', 'ZONE 4 FILTER']

    def __init__(self,program,index):
        pass

