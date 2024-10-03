import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine
import tensorflow as tf
from keras.layers import TFSMLayer
from .preprocess import get_fft_spectrum
from pyaudio import paInt16

# Signal processing constants
SAMPLE_RATE = 16000
PREEMPHASIS_ALPHA = 0.97
FRAME_LEN = 0.025
FRAME_STEP = 0.01
NUM_FFT = 512
BUCKET_STEP = 1
MAX_SEC = 10

# Model and embedding constants
MODEL_FILE = "voice_auth_model_cnn"
COST_METRIC = "cosine"  # euclidean or cosine
INPUT_SHAPE = (NUM_FFT, None, 1)

# IO
EMBED_LIST_FILE = "data/embed"

# Recognition
THRESHOLD = 0.35

def buckets(max_time, steptime, frameskip):
    buckets = {}
    frames_per_sec = int(1/frameskip)
    end_frame = int(max_time*frames_per_sec)
    step_frame = int(steptime*frames_per_sec)
    for i in range(0, end_frame+1, step_frame):
        s = i
        s = np.floor((s-7+2)/2) + 1  # for first conv layer
        s = np.floor((s-3)/2) + 1    # for first maxpool layer
        s = np.floor((s-5+2)/2) + 1  # for second conv layer
        s = np.floor((s-3)/2) + 1    # for second maxpool layer
        s = np.floor((s-3+2)/1) + 1  # for third conv layer
        s = np.floor((s-3+2)/1) + 1  # for fourth conv layer
        s = np.floor((s-3+2)/1) + 1  # for fifth conv layer
        s = np.floor((s-3)/2) + 1    # for fifth maxpool layer
        s = np.floor((s-1)/1) + 1    # for sixth fully connected layer
        if s > 0:
            buckets[i] = int(s)
    return buckets

def get_embedding(model, wav_file, max_time):
    buckets_var = buckets(MAX_SEC, BUCKET_STEP, FRAME_STEP)
    signal = get_fft_spectrum(wav_file, buckets_var)
    embedding = np.squeeze(model(signal.reshape(1, *signal.shape, 1)))
    return embedding

def get_embedding_batch(model, wav_files, max_time):
    return [get_embedding(model, wav_file, max_time) for wav_file in wav_files]

def get_embeddings_from_list_file(model, list_file, max_time):
    buckets_var = buckets(MAX_SEC, BUCKET_STEP, FRAME_STEP)
    result = pd.read_csv(list_file, delimiter=",")
    result['features'] = result['filename'].apply(lambda x: get_fft_spectrum(x, buckets_var))
    result['embedding'] = result['features'].apply(lambda x: np.squeeze(model(x.reshape(1, *x.shape, 1))))
    return result[['filename', 'speaker', 'embedding']]