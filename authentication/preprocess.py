import librosa
import numpy as np
from scipy.signal import lfilter
from python_speech_features import sigproc
import logging

# Signal processing
SAMPLE_RATE = 16000
PREEMPHASIS_ALPHA = 0.97
FRAME_LEN = 0.025
FRAME_STEP = 0.01
NUM_FFT = 512
BUCKET_STEP = 1
MAX_SEC = 10

# Model
MODEL_FILE = "voice_auth_model_cnn"
COST_METRIC = "cosine"  # euclidean or cosine
INPUT_SHAPE = (NUM_FFT, None, 1)

# IO
EMBED_LIST_FILE = "data/embed"

# Recognition
THRESHOLD = 0.35

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def load(filename, sample_rate):
    audio, sr = librosa.load(filename, sr=sample_rate, mono=True)
    audio = audio.flatten()
    return audio

def normalize_frames(m, epsilon=1e-12):
    return np.array([(v - np.mean(v)) / max(np.std(v), epsilon) for v in m])

def remove_dc_and_dither(sin, sample_rate):
    if sample_rate == 16e3:
        alpha = 0.99
    elif sample_rate == 8e3:
        alpha = 0.999
    else:
        logging.error("Sample rate must be 16kHz or 8kHz only")
        exit(1)
    sin = lfilter([1, -1], [1, -alpha], sin)
    dither = np.random.random_sample(len(sin)) + np.random.random_sample(len(sin)) - 1
    spow = np.std(dither)
    sout = sin + 1e-6 * spow * dither
    return sout

def get_fft_spectrum(filename, buckets):
    signal = load(filename, SAMPLE_RATE)
    signal *= 2 ** 15

    # get FFT spectrum
    signal = remove_dc_and_dither(signal, SAMPLE_RATE)
    signal = sigproc.preemphasis(signal, coeff=PREEMPHASIS_ALPHA)
    frames = sigproc.framesig(signal, frame_len=FRAME_LEN * SAMPLE_RATE, frame_step=FRAME_STEP * SAMPLE_RATE, winfunc=np.hamming)
    fft = abs(np.fft.fft(frames, n=NUM_FFT))
    fft_norm = normalize_frames(fft.T)

    logging.debug(f"FFT Norm Shape: {fft_norm.shape}")

    if fft_norm.shape[1] == 0:
        logging.error("FFT norm has no columns. Possible empty or corrupted audio file.")
        return np.array([])

    valid_buckets = [k for k in buckets if k <= fft_norm.shape[1]]
    if not valid_buckets:
        logging.error("No valid bucket sizes for the given FFT norm shape.")
        return np.array([])

    rsize = max(valid_buckets)
    rstart = int((fft_norm.shape[1] - rsize) / 2)
    out = fft_norm[:, rstart:rstart + rsize]

    return out