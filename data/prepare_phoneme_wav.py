
#!/usr/bin/env python

import errno
import os
from os import path
import sys
import tarfile
import fnmatch
import pandas as pd
import subprocess
from pydub import AudioSegment

kbits = 16

def split_wav_file(rif_file, phn_file):
    print(rif_file)
    audio = AudioSegment.from_wav(rif_file)
    file_base = rif_file[:-8]
    with open(phn_file) as fp:
       line = fp.readline()
       while line:
           columns = line.strip().split(' ')
           start = int(columns[0]) // kbits
           stop = int(columns[1]) // kbits
           phoneme = columns[2]
           # print("start: {}, stop: {}, size: {}".format(start, stop, len(audio)))
           new_file_path = file_base + "ph_" + phoneme + "_ph.wav"
           # Process segment
           segment_audio = audio[start:stop]
           segment_audio.export(new_file_path, format="wav")
           line = fp.readline()

def _preprocess_data(args):

    # Assume data is downloaded from LDC - https://catalog.ldc.upenn.edu/ldc93s1

    datapath = args
    target = path.join(datapath, "TIMIT")
    print("Checking to see if data has already been extracted in given argument: %s", target)

    if not path.isdir(target):
        print("Could not find extracted data, trying to find: TIMIT-LDC93S1.tgz in: ", datapath)
        filepath = path.join(datapath, "TIMIT-LDC93S1.tgz")
        if path.isfile(filepath):
            print("File found, extracting")
            tar = tarfile.open(filepath)
            tar.extractall(target)
            tar.close()
        else:
            print("File should be downloaded from LDC and placed at:", filepath)
            strerror = "File not found"
            raise IOError(errno, strerror, filepath)

    else:
        # is path therefore continue
        print("Found extracted data in: ", target)

    print("Preprocessing data")
    for root, dirnames, filenames in os.walk(target):
        for filename in fnmatch.filter(filenames, "*.WAV"):
            wav_file = os.path.join(root, filename)
            rif_file = os.path.join(root, filename)[:-4] + "_rif.wav"
            phn_file = os.path.join(root, filename)[:-4] + ".PHN"
            split_wav_file(rif_file, phn_file)

if __name__ == "__main__":
    _preprocess_data(sys.argv[1])
    print("Completed")
