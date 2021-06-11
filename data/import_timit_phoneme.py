#!/usr/bin/env python

'''
    NAME    : LDC TIMIT Dataset
    URL     : https://catalog.ldc.upenn.edu/ldc93s1
    HOURS   : 5
    TYPE    : Read - English
    AUTHORS : Garofolo, John, et al.
    TYPE    : LDC Membership
    LICENCE : LDC User Agreement
'''




import errno
import os
from os import path
import sys
import tarfile
import fnmatch
import pandas as pd
import subprocess

def clean(word):
    # LC ALL & strip punctuation which are not required
    new = word.lower().replace('.', '')
    new = new.replace(',', '')
    new = new.replace(';', '')
    new = new.replace('"', '')
    new = new.replace('!', '')
    new = new.replace('?', '')
    new = new.replace(':', '')
    new = new.replace('-', '')
    return new

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

    print("Building CSVs")

    # Lists to build CSV files
    train_list_wavs, train_list_trans, train_list_size = [], [], []
    test_list_wavs, test_list_trans, test_list_size = [], [], []

    for root, dirnames, filenames in os.walk(target):
        for filename in fnmatch.filter(filenames, "*_ph.wav"):

            full_wav = os.path.join(root, filename)
            wav_filesize = path.getsize(full_wav)
            file_part = filename.split("_")
            trans = file_part[1]

            if 'train' in full_wav.lower():
                train_list_wavs.append(full_wav)
                train_list_trans.append(trans)
                train_list_size.append(wav_filesize)
            elif 'test' in full_wav.lower():
                test_list_wavs.append(full_wav)
                test_list_trans.append(trans)
                test_list_size.append(wav_filesize)
            else:
                raise IOError

    a = {'wav_filename': train_list_wavs,
         'wav_filesize': train_list_size,
         'transcript': train_list_trans
         }

    c = {'wav_filename': test_list_wavs,
         'wav_filesize': test_list_size,
         'transcript': test_list_trans
         }

    all = {'wav_filename': train_list_wavs + test_list_wavs,
          'wav_filesize': train_list_size + test_list_size,
          'transcript': train_list_trans + test_list_trans
          }

    df_all = pd.DataFrame(all, columns=['wav_filename', 'wav_filesize', 'transcript'], dtype=int)
    df_train = pd.DataFrame(a, columns=['wav_filename', 'wav_filesize', 'transcript'], dtype=int)
    df_test = pd.DataFrame(c, columns=['wav_filename', 'wav_filesize', 'transcript'], dtype=int)

    df_all.to_csv(target+"/timit_phoneme_all.csv", sep=',', header=True, index=False, encoding='ascii')
    df_train.to_csv(target+"/timit_phoneme_train.csv", sep=',', header=True, index=False, encoding='ascii')
    df_test.to_csv(target+"/timit_phoneme_test.csv", sep=',', header=True, index=False, encoding='ascii')

if __name__ == "__main__":
    _preprocess_data(sys.argv[1])
    print("Completed")
