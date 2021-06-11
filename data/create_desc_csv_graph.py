"""
Use this script to create JSON-Line description files that can be used to
train deep-speech models through this library.
This works with data directories that are organized like LibriSpeech:
data_directory/group/speaker/[file_id1.wav, file_id2.wav, ...,
                              speaker.trans.txt]

Where speaker.trans.txt has in each line, file_id transcription
"""

from __future__ import absolute_import, division, print_function

import argparse
import json
import wave
import os
import glob
import pandas as pd
import python_speech_features as p
import scipy.io.wavfile as wav

def main(data_directory, output_file):
    labels = []
    filesizes = []
    keys = []
    for group in os.listdir(data_directory):
        if group.startswith('.'):
            continue
        speaker_path = os.path.join(data_directory, group)
        print(speaker_path)
        for wav_file in glob.glob(speaker_path + "/*.wav"):
            sfile = os.path.basename(wav_file).split("_")
            word = sfile[1]
            voice = sfile[2]
            locale = sfile[3]
            try:
                phoneme = word.lower()
                print(f"{word} - {voice} - {locale} - {phoneme} -")
                audio_file =  wav_file
                print(audio_file)
                filesize = os.stat(audio_file).st_size
                keys.append(audio_file)
                filesizes.append(filesize)
                labels.append(phoneme)
            except Exception as e:
                print(e)
        df_ = pd.DataFrame()
        df_["transcript"] = labels
        df_["wav_filename"] = keys
        df_["wav_filesize"] = filesizes
        df_.to_csv(output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_directory', type=str,
                        help='Path to data directory')
    parser.add_argument('output_file', type=str,
                        help='Path to output file')
    args = parser.parse_args()
    main(args.data_directory, args.output_file)
