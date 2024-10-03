import cv2
import math
from sklearn import neighbors
import os
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate("brailleproject-8091a-firebase-adminsdk-fnggw-c19e1f8fde.json")  # Path to your service account key JSON file
firebase_admin.initialize_app(cred, {
    'storageBucket': 'brailleproject-8091a.appspot.com'
})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG'}

def download_images_from_firebase(bucket_name, local_dir, folder_name='AUTH'):
    bucket = storage.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_name)

    for blob in blobs:
        if not blob.name.endswith('/'):  # Ignore directories
            filename = os.path.join(local_dir, os.path.relpath(blob.name, folder_name))
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            try:
                blob.download_to_filename(filename)
                print(f'Downloaded {blob.name} to {filename}')
            except Exception as e:
                print(f'Failed to download {blob.name}: {e}')

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    X = []
    y = []

    for person_dir in os.listdir(train_dir):
        person_path = os.path.join(train_dir, person_dir)
        if not os.path.isdir(person_path):
            continue

        images_dir = os.path.join(person_path, "Image")
        if not os.path.exists(images_dir):
            continue

        for img_path in image_files_in_folder(images_dir):
            print(f"Processing image: {img_path}")
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                if verbose:
                    print(f"Image {img_path} not suitable for training: {'Didn''t find a face' if len(face_bounding_boxes) < 1 else 'Found more than one face'}")
                continue

            X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            y.append(person_dir)

    if len(X) == 0:
        raise ValueError("No valid face encodings found in the training data. Ensure the images contain faces.")

    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf

def predict(X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either through knn_clf or model_path")

    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    if len(X_face_locations) == 0:
        return []

    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def KNN_response(input_image_path):
    print(input_image_path)

    # Get the directory where the current script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_dir = os.path.join(current_dir, "tempfb/AUTH")

    print(f"Downloading images from Firebase Storage to {local_dir}...")
    download_images_from_firebase('brailleproject-8091a.appspot.com', local_dir, folder_name='Authen2')
    print("Download complete!")

    print("Training KNN classifier...")
    try:
        train(local_dir, model_save_path="trained_knn_model.clf", n_neighbors=2, verbose=True)
        print("Training complete!")
    except ValueError as e:
        print(f"Error during training: {e}")
        return []

    frame = cv2.imread(input_image_path)
    img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    predictions = predict(img, model_path="trained_knn_model.clf")
    print(f"Predictions for {input_image_path}: {predictions}")

    return predictions
