# Speech butler phoneme

This project tries to train a Deep Learning model using TIMIT corpus.

With TIMIT corpus the model can be trained with phonemes outputs instead letters. The reason is that TIMIT has the phoneme sound boundaries set correctly.


## Installation

1. Clone repo
2. Copy TIMIT corpus into `data` subdirectory.
3. Prepare data with this command: `python3 import_timit.py ~/projects/speechbutlerphoneme/data`
4. Train with: `nohup python3 run-train.py --train_files data/TIMIT/timit_train.csv --valid_files data/TIMIT/timit_test.csv --fc_size 512 --epochs 200 --rnn_size 512 > keras.log &`
    or
    `nohup python3 run-train.py --train_files data/TIMIT/timit_train_bolt.csv --valid_files data/TIMIT/timit_test_bolt.csv --fc_size 512 --epochs 200 --rnn_size 512 > keras.log &`
      or  
      `nohup python3 run-train.py --train_files data/TIMIT/timit_phoneme_train_bolt.csv --valid_files data/TIMIT/timit_phoneme_test_bolt.csv --fc_size 2048 --epochs 200 --rnn_size 2048 > keras.log &`