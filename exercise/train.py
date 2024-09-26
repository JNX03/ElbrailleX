# train.py

import tensorflow as tf
import librosa
import numpy as np
from .models import AudioModel

def preprocess_audio(audio_path):
    # Load and preprocess the audio file
    audio, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)
    mfcc = mfcc[np.newaxis, ..., np.newaxis]
    return mfcc

def retrain_model(audio_path, label):
    # Load existing model
    model_path = 'alphabet_recognition_model.h5'
    model = tf.keras.models.load_model(model_path)

    # Preprocess the new audio data
    mfcc = preprocess_audio(audio_path)
    label_index = ord(label.lower()) - ord('a')  # Convert label to index
    y_new = tf.keras.utils.to_categorical(label_index, num_classes=26)  # Assuming 26 classes for a-z

    # Retrain the model
    model.fit(mfcc, np.array([y_new]), epochs=1)

    # Save the updated model
    model.save(model_path)

    return True  # Return success status
