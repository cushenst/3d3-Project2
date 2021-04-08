#!/usr/bin/env python3

import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from aubio import float_type, pitch

try:
    columns, _ = shutil.get_terminal_size()
except AttributeError:
    columns = 80

# select sample rate. 20 works well in quiet environments
block_duration = 20
# select microphone
print(sd.query_devices())
device = int(input("Please select Microphone:\t"))
# set gain
gain = 1.0
# set frequence range expected
f_range = [100, 5000]
# downsample to run on less powerful computers
downsample = 1

low, high = f_range
if high <= low:
    print('HIGH must be greater than LOW')
    sys.exit()

# get microphone sample rate
samplerate = sd.query_devices(device, 'input')['default_samplerate'] // downsample

win_s = 4096  # fft size
hop_s = 1024  # hop size

tolerance = 0.7
# set the ± frequency between symbols
f_tolerance = 20

# set base frequency. Must match transmitter.
base_frequency = 1200
# set pitch detection algorithm
pitch_o = pitch("yinfast", win_s, hop_s, int(samplerate))
# set pitch units
pitch_o.set_unit("Hz")
# pitch_o.set_silence(-40)
# set tolerence needed
pitch_o.set_tolerance(tolerance)
pitches = []
confidences = []
total_frames = 1


# convert symbols received to binary
def mod2bin(number):
    print(number)
    cases = {
        0.66: "000",
        1: "001",
        1.33: "010",
        1.5: "01",
        1.66: "011",
        2: "100",
        2.33: "101",
        2.5: "11",
        2.66: "110",
        3: "111",
        3.33: ""
    }
    binary = cases.get(number)
    return binary


def callback(indata, frames, time, status):
    global pitches
    global confidences
    global total_frames
    data_found = False
    if status:
        print(status)
    if any(indata):
        data = np.zeros(hop_s)
        for i in range(len(indata)):
            data[i] = indata[i][0]
        pad_length = pitch_o.hop_size - data.shape[0] % pitch_o.hop_size
        data_padded = np.pad(data, (0, pad_length), 'constant', constant_values=0)
        data_padded = data_padded.reshape(-1, pitch_o.hop_size)
        data_padded = data_padded.astype(float_type)
        for frame, i in zip(data_padded, range(len(data_padded))):
            time_str = "%.3f" % (i * pitch_o.hop_size / float(samplerate))
            # get pitch
            pitch = pitch_o(frame)[0]
            confidence = pitch_o.get_confidence()
            values = [0.66, 1, 1.33, 1.66, 2, 2.33, 2.66, 3, 3.33]
            for a in values:
                if (f_tolerance + base_frequency * a) > pitch > (base_frequency * a - f_tolerance):
                    pitches += [a]
                    data_found = True
                    break
            if data_found:
                print("%s %f %f" % (time_str, pitch, confidence))
                confidences += [confidence]
                total_frames += 0.5
    else:
        print('no input')


with sd.InputStream(device=device, channels=1, callback=callback,
                    blocksize=int(samplerate * block_duration / 1000),
                    samplerate=samplerate):
    print(samplerate)
    while True:
        response = input()
        if response in ('', 'q', 'Q'):
            break

pitches = np.array(pitches[1:])

print(pitches)
stringOfValues = ""
stringOfEncodedValues = ""

bit_count = 0
for i in range(1, len(pitches)):
    if pitches[i] != pitches[i - 1]:
        stringOfEncodedValues += str(float(pitches[i]))
        stringOfEncodedValues += " "
        if pitches[i] == 3.33:
            if len(stringOfValues) != 0:
                print(stringOfValues)
                stringOfValues += stringOfValues[len(stringOfValues) - 3]
                stringOfValues += stringOfValues[len(stringOfValues) - 3]
                stringOfValues += stringOfValues[len(stringOfValues) - 3]
        else:
            stringOfValues += mod2bin(float(pitches[i]))

listOfValues = [stringOfValues[i:i + 7] for i in range(0, len(stringOfValues), 7)]

binaryString = ""

for i in listOfValues:
    binaryString += i
    binaryString += " "

print(stringOfEncodedValues)
print(binaryString)
print(listOfValues)
decodedText = ""

for i in listOfValues:
    decodedText += chr(int(i, 2))
print(decodedText)
confidences = np.array(confidences[1:])
times = [t * hop_s for t in range(len(pitches))]
