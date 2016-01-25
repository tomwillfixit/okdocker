#!/usr/bin/env python2.7
VERSION = "0.1"
"""

Author : Thomas Shaw
Date   : Jan 2016
Description :

Ok Docker will record 3 seconds of speech, decode to text and then attempt to match to a known docker command based on a list of supported actions*.  If a match is found then the command will be run.  The container in which this code runs must have access to the hosts sound libraries, run as priviledged and be able to run docker commands on the host.  Details in Dockerfile.

*Comparing to a list of known docker commands hasn't be done yet.  Currently Ok Docker just records and decodes to text.

"""

import os
import sys
import optparse

import pyaudio
import wave
import sphinxbase

# Import occasionally fails first time
try:
    import pocketsphinx
except ValueError:
    import pocketsphinx

CWD = str(os.path.dirname(os.path.realpath(__file__)))

# Paths : Language models and dictionary required by pocketsphinx US English
# Does not support Northern Irish accent
 
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
HMDIR = os.path.join(BASE_PATH, "hmm/cmusphinx-en-us-5.2")
LMDIR = os.path.join(BASE_PATH, "lm/cmusphinx-5.0-en-us.lm")
DICTD = os.path.join(BASE_PATH, "dict/cmu07a.dic")

def header():
    print('''
===========================================================================
Ok Docker (Version : %s)
===========================================================================
''' % (VERSION))

def print_usage():
    """ This function will print out okdocker usage. """

    header()
    print '''
    Command Line Usage :

        ./okdocker.py --option <argument>

    Options :

	record < .wav filename >
	playback < .wav filename >
	decode < .wav filename >

        demo (Recording and decoding demo)
    '''

def validate():
    '''Validates the options passed in on the command line and stores them.'''

    global arguments, version, usage, record, play, decode, demo

    arguments = sys.argv[1:]

    #simple check to catch missing -- early
    required = '--'
    result = [y for y in arguments if required in y]
    if not result:
        print("[ERROR] ... Option should be preceded by --.")
        sys.exit(2)

    parser = optparse.OptionParser(add_help_option=False)

    parser.add_option('--usage',
                      dest="usage",
                      default=False,
                      action="store_true",
                      help="Displays Usage.",
    )

    parser.add_option('--version',
                      dest="version",
                      default=False,
                      action="store_true",
                      help="Displays Version number.",
    )


    parser.add_option('--record',
                      dest="record",
                      default="",
                      help="Record 3 second sound clip and store in .wav file",
    )

    parser.add_option('--play',
                      dest="play",
                      default="",
                      help="Playback sound clip from .wav file",
    )

    parser.add_option('--decode',
                      dest="decode",
                      default="",
                      help="Decode .wav file to text",
    )

    parser.add_option('--demo',
                      dest="demo",
                      default="False",
		      action="store_true",
                      help="Records and Decodes .wav file to text",
    )

    options, remainder = parser.parse_args()

    version = options.version
    usage = options.usage
    record = options.record
    play = options.play
    decode = options.decode
    demo = options.demo

    #Checks to catch input not handled by optparse.
    #if no arguments are passed in then display menu.
    if len(arguments) == 0:
        print_usage()
        sys.exit(0)

    if version:
        print VERSION
        sys.exit(0)

    if usage:
        print_usage()
        sys.exit(0)


def validate_file(filename):
    """Check file exists"""

    if not os.path.exists(filename):
	print "Filename : %s does not exist.  Exiting." %(filename)
	sys.exit(2)


def start_recording(filename):
    """Record a short section of audio"""

    CHUNK = 128
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3
    
    filename = "%s/wav/%s" %(CWD, filename)

    print "Recording will be stored in : %s" %(filename)
    print "Recording will start in 3 seconds"
    os.system("sleep 3")

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("*** Recording Now ***")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("*** Finished Recording ***")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_recording(filename):
    """ Playback recording """

    CHUNK = 128

    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()


def decode_recording(filename):
    """ Decode recording """

    recognition = pocketsphinx.Decoder(hmm=HMDIR, lm=LMDIR, dict=DICTD)
    filename = file(filename, 'rb')
    filename.seek(44)
    print "debug"
    recognition.decode_raw(filename)
    command = recognition.get_hyp()

    return command 



#start here

def main():
    validate()
    header()

    print('''

---> Selected     : %s
---------------------------------------------------------------------------
''' % (arguments))
    
    if record:
        start_recording(record)

    if play:
        validate_file(play)
	play_recording(play)

    if decode:
        validate_file(decode)
        command = decode_recording(decode)
        print "You have requested Docker to : {0}".format(command[0])
        #todo : verify docker command against list of supported commands

    if demo:
        demo_recording="demo.wav"
        start_recording(demo_recording)
        validate_file("wav/%s" %(demo_recording))
        command = decode_recording("wav/%s" %(demo_recording))
        print "DEMO : You have requested Docker to : {0}".format(command[0]) 

if __name__ == '__main__':
    main()
