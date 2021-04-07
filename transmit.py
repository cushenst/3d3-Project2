#!/usr/bin/env python3

import math
import time

import numpy as np
import sounddevice as sd


def send_over_sound(message):
    # set device to play sound from
    sd.default.device = 3  # int(input("Please select Microphone:\t"))
    # Samples per second
    sps = 44100
    spp = int(2560 * 2.5)

    # Base Frequency that must match receiver
    freq_hz = 1200.0

    # Attenuation so the sound is reasonable volume
    atten = 0.1

    # Convert message to binary.
    message_binary = ' '.join(f"{ord(x):07b}" for x in message)
    print(message_binary)
    message_binary = message_binary.replace(" ", "")
    print(len(message_binary))

    # make sure the message is divisible by 3 for encoding
    while (len(message_binary) % 3 != 0):
        message_binary += "0"

    # print message in binary
    print([message_binary[i:i + 7] for i in range(0, len(message_binary), 7)])

    message_binary_list = [3.33, 3.33]

    # encode message no symbols beside each other will be the same.
    for i in range(0, len(message_binary), 3):
        if message_binary[i] == "0" and message_binary[i + 1] == "0" and message_binary[i + 2] == "0":
            message_binary_list.append(0.66)
        elif message_binary[i] == "0" and message_binary[i + 1] == "0" and message_binary[i + 2] == "1":
            message_binary_list.append(1)
        elif message_binary[i] == "0" and message_binary[i + 1] == "1" and message_binary[i + 2] == "0":
            message_binary_list.append(1.33)
        elif message_binary[i] == "0" and message_binary[i + 1] == "1" and message_binary[i + 2] == "1":
            message_binary_list.append(1.66)
        elif message_binary[i] == "1" and message_binary[i + 1] == "0" and message_binary[i + 2] == "0":
            message_binary_list.append(2)
        elif message_binary[i] == "1" and message_binary[i + 1] == "0" and message_binary[i + 2] == "1":
            message_binary_list.append(2.33)
        elif message_binary[i] == "1" and message_binary[i + 1] == "1" and message_binary[i + 2] == "0":
            message_binary_list.append(2.66)
        elif message_binary[i] == "1" and message_binary[i + 1] == "1" and message_binary[i + 2] == "1":
            message_binary_list.append(3)
        transmit_lenght = len(message_binary_list)
        if message_binary_list[transmit_lenght - 2] == message_binary_list[transmit_lenght - 1]:
            message_binary_list[transmit_lenght - 1] = 3.33

    print(message_binary_list)

    # NumpPy to calculate the waveform
    # Calculate the duration of the message
    duration_s = ((len(message_binary_list)) * spp) / sps
    duration_s = math.ceil(duration_s)
    print(duration_s)
    # Calculate the number of samples
    total_samples = sps * duration_s

    each_sample_number = np.arange(total_samples)

    # convert message list to numpy array
    message_array = np.array(message_binary_list)
    scaled_message_array = np.array([0, 0])

    # Scale message to have spp samples per symbol
    for i in message_binary_list:
        a = np.full((1, spp), i)
        scaled_message_array = np.concatenate((scaled_message_array, np.full((1, spp), i)), axis=None)

    # pad message with zeros to ensure array is full
    scaled_message_array = np.pad(scaled_message_array, (0, total_samples - len(scaled_message_array)), "constant")
    # set symbol frequency
    message_array = scaled_message_array * freq_hz
    # calculate waveform
    waveform = np.sin(2 * np.pi * each_sample_number * message_array / sps)
    # lower volume
    waveform_quiet = waveform * atten
    # generate graph for debug
    # plt.title("Matplotlib demo")
    # plt.xlabel("x axis caption")
    # plt.ylabel("y axis caption")
    # plt.plot(each_sample_number, waveform_quiet)
    # dont show graph
    # plt.show()

    # Play the waveform out the speakers
    sd.play(waveform_quiet, sps)
    time.sleep(duration_s)
    sd.stop()
    return

