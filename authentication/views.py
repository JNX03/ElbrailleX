import os
import time
import json
import logging
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials, storage, initialize_app
from .FaceKNN import KNN_response
import firebase_admin
from pathlib import Path
import base64
import cv2
import subprocess

filepath = "C:/Users/jeans/Desktop/LastEbail/EIBraille-Webapplication-1.1/eibraille"
logging.basicConfig(level=logging.DEBUG)

@csrf_exempt
def save_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        username = request.POST.get('username', 'anonymous')

        parent_dir = Path(__file__).resolve().parent.parent
        sound_dir = parent_dir / 'sound'
        sound_dir.mkdir(parents=True, exist_ok=True)
        file_path = sound_dir / f'{username}-audio.wav'

        with open(file_path, 'wb+') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        return JsonResponse({'message': 'Audio saved successfully', 'path': str(file_path)})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

firebase_key_path = os.path.join(settings.BASE_DIR, 'authentication', 'brailleproject-8091a-firebase-adminsdk-fnggw-c19e1f8fde.json')

cred = credentials.Certificate(firebase_key_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'brailleproject-8091a.appspot.com'
    })
@csrf_exempt
def train(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        if not username:
            logging.error('Username is required')
            return JsonResponse({'error': 'Username is required'}, status=400)

        file_path = f"Authen2/{username}/{username}-audio.wav"

        try:
            bucket = storage.bucket()
            blob = bucket.blob(file_path)

            temp_file = f"C:/Users/jeans/Desktop/LastEbail/EIBraille-Webapplication-1.1/eibraille/sound/{username}-audio.wav"
            
            if not blob.exists():
                logging.error(f'File {file_path} not found in bucket')
                return JsonResponse({'error': f'File {file_path} not found in bucket'}, status=404)

            logging.info(f'Downloading file {file_path} to {temp_file}')
            blob.download_to_filename(temp_file)

            logging.info('Running voice_auth.py script')
            result = subprocess.run(
                ["python", "voice_auth.py", "-t", "enroll", "-n", username, "-f", temp_file],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logging.error(f"Voice auth script error: {result.stdout}")
                return JsonResponse({'error': result.stderr, 'stdout': result.stdout}, status=500)

            logging.info('User enrolled successfully')
            return JsonResponse({'message': 'User enrolled successfully', 'stdout': result.stdout})
        
        except Exception as e:
            logging.error(f"Exception during enrollment: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    logging.error('Invalid request method')
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        try:
            if 'audio' not in request.FILES:
                return JsonResponse({'error': 'Audio file is required'}, status=400)

            audio_file = request.FILES['audio']
            
            # Define the temporary directory and file path
            temp_dir = os.path.join(settings.BASE_DIR, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_file = os.path.join(temp_dir, audio_file.name)

            # Save the uploaded audio file to a temporary location
            with open(temp_file, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # Run the voice_auth.py script with the recognize command
            result = subprocess.run(
                ["python", "voice_auth.py", "-t", "recognize", "-f", temp_file],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logging.error(f"Voice auth script error: {result.stderr}")
                return JsonResponse({'error': result.stderr}, status=500)

            # On success, return a success message
            return JsonResponse({'message': 'Recognition completed successfully', 'redirect': '/home/'})
        
        except Exception as e:
            logging.error(f"Exception during recognition: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def process_photo(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
    try:
        # Parse the incoming request body as JSON
        request_data = json.loads(request.body)
        file_path = request_data.get('filepath')

        if not file_path:
            return JsonResponse({'error': 'File path not provided.'}, status=400)
        
        # Log the received file path
        logging.debug(f"Received file path: {file_path}")

        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"File does not exist: {file_path}")
            return JsonResponse({'error': 'File does not exist.'}, status=400)

        # Load the image
        image = cv2.imread(file_path)
        
        # Check if the image is loaded correctly
        if image is None:
            logging.error(f"Error loading image: {file_path}")
            return JsonResponse({'error': 'Error loading image.'}, status=500)
        
        # Perform prediction using KNN_response function
        prediction = KNN_response(file_path)
        return JsonResponse({'message': prediction})
    except Exception as e:
        logging.error(f"Error processing photo: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('dataURL')
            
            if not image_data:
                return JsonResponse({'error': 'No image data provided'}, status=400)
            
            header, encoded = image_data.split(',', 1)
            image_data = base64.b64decode(encoded)
            
            parent_dir = Path(__file__).resolve().parent.parent
            image_dir = parent_dir / 'tempfb'
            image_dir.mkdir(parents=True, exist_ok=True)
            file_path = image_dir / f'{int(time.time())}-image.png'
            
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            logging.debug(f"Image saved at {file_path}")
            return JsonResponse({'message': 'Image saved successfully', 'path': str(file_path)})
        except Exception as e:
            logging.error(f"Error saving image: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def welcome_page(request):
    return render(request, 'index.html')

def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home.html")

def tab_action_page(request):
    return render(request, 'login.html')

def h_page(request):
    return render(request, 'signup.html')

def portals(request):
    return render(request, 'portals.html')

