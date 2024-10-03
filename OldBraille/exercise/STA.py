import numpy as np
import tensorflow as tf
import librosa

def load_model(model_path):
    return tf.keras.models.load_model(model_path)

def predict_audio(model, audio_path):
    audio, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)
    
    mfcc = mfcc[np.newaxis, ..., np.newaxis]
    mfcc = mfcc / 255.0 

    prediction = model.predict(mfcc)
    return np.argmax(prediction)

def predict_alphabet(audio_path):
    model_path = 'alphabet_recognition_model.h5'
    model = load_model(model_path)
    prediction = predict_audio(model, audio_path)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return alphabet[prediction]
