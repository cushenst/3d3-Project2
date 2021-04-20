# Project 2 Group 19

Trinity College Dublin CSU33D03 Computer Networks - Emergency Alert TCP Transmission with Audio Transmission Fallback

## Description

Codebase consists of server Pythons script as well as client-receiver script with accompanying audio receive and transmit scripts used by the receiver as audio fallback in cases of connection error or disconnection from TCP server.

## Installation

Python libraries required are in requirements.txt file. Use pip to install the required libraries.

```bash
pip install numpy
pip install sounddevice
pip install matplotlib
pip install aubio
```

## Usage

Server HOST and receiver SERVER variables should be changed to the appropriate IPv6 address being used.

Before running receiver, sound devices in transmit.py and audio-receiver.py need to be set to the speaker and microphone sound device numbers of the computer.

Device numbers of the computer can be found by running the code below in a Python shell.

```python
import sounddevice
sounddevice.query_devices()
```

Once the server is running within the server terminal, "help" can be inputted to obtain the available commands.