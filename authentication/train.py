
import os
import firebase_admin
from firebase_admin import credentials, storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from voice_auth import enroll 

cred = credentials.Certificate("brailleproject-8091a-firebase-adminsdk-fnggw-c19e1f8fde.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'brailleproject-8091a.appspot.com'
})

@csrf_exempt
def train(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        file_path = f"Authen2/{username}-audio.wav"

        try:
            bucket = storage.bucket()
            blob = bucket.blob(file_path)

            temp_file = f"/tmp/{username}-audio.wav"
            blob.download_to_filename(temp_file)

            enroll(username, temp_file)

            return JsonResponse({'message': 'User enrolled successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
