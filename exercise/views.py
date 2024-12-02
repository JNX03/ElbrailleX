from django.shortcuts import render
from django.http import JsonResponse
from .STA import predict_alphabet
import os
from django.conf import settings
from django.http import HttpResponse
from gtts import gTTS
from django.views.decorators.csrf import csrf_exempt
from .models import AudioModel
import os
from .STT import correction_system

def practice(request, n):
    if n == 1:
        return render(request, "exercise1.html") #use to be ex1.html
    elif n == 26:
        return render(request, "exercise2.html") #use to be ex2.html

    # Define the braille pattern for the letter
    braille_patterns = {
        'a': [1, 0, 0, 0, 0, 0],
        'b': [1, 1, 0, 0, 0, 0],
        'c': [1, 0, 0, 1, 0, 0],
        'd': [1, 0, 0, 1, 1, 0],
        'e': [1, 0, 0, 0, 1, 0],
        'f': [1, 1, 0, 1, 0, 0],
        'g': [1, 1, 0, 1, 1, 0],
        'h': [1, 1, 0, 0, 1, 0],
        'i': [0, 1, 0, 1, 0, 0],
        'j': [0, 1, 0, 1, 1, 0],
        'k': [1, 0, 1, 0, 0, 0],
        'l': [1, 1, 1, 0, 0, 0],
        'm': [1, 0, 1, 1, 0, 0],
        'n': [1, 0, 1, 1, 1, 0],
        'o': [1, 0, 1, 0, 1, 0],
        'p': [1, 1, 1, 1, 0, 0],
        'q': [1, 1, 1, 1, 1, 0],
        'r': [1, 1, 1, 0, 1, 0],
        's': [0, 1, 1, 1, 0, 0],
        't': [0, 1, 1, 1, 1, 0],
        'u': [1, 0, 1, 0, 0, 1],
        'v': [1, 1, 1, 0, 0, 1],
        'w': [0, 1, 0, 1, 1, 1],
        'x': [1, 0, 1, 1, 0, 1],
        'y': [1, 0, 1, 1, 1, 1],
        'z': [1, 0, 1, 0, 1, 1],
    }

    letter = chr(ord('a') - 1 + n)
    context = {
        "n": n,
        "n_prev": n - 1,
        "n_next": n + 1,
        "letter": letter,
        "braille_pattern": braille_patterns.get(letter, [0, 0, 0, 0, 0, 0])
    }
    request.session['n_index'] = n
    return render(request, "exercise.html", context)


letter_variations = {
    'a': ['a', 'ay'],
    'b': ['b', 'bee', 'be'],
    'c': ['c', 'see', 'sea'],
    'd': ['d', 'dee', 'de', 'dea'],
    'e': ['e', 'ee'],
    'f': ['f', 'ef', 'eff'],
    'g': ['g', 'gee', 'ge'],
    'h': ['h', 'aitch', 'ache'],
    'i': ['i', 'eye', 'aye'],
    'j': ['j', 'jay'],
    'k': ['k', 'kay'],
    'l': ['l', 'el', 'ell'],
    'm': ['m', 'em', 'emm'],
    'n': ['n', 'en', 'enn'],
    'o': ['o', 'oh'],
    'p': ['p', 'pee', 'pe'],
    'q': ['q', 'queue'],
    'r': ['r', 'ar', 'arr'],
    's': ['s', 'ess', 'es'],
    't': ['t', 'tee', 'te'],
    'u': ['u', 'you', 'yew'],
    'v': ['v', 'vee', 've'],
    'w': ['w', 'double-u'],
    'x': ['x', 'ex'],
    'y': ['y', 'why', 'wy'],
    'z': ['z', 'zee', 'zed']
}

def normalize_answer(answer):
    answer = answer.lower()
    for key, variations in letter_variations.items():
        for variation in variations:
            if answer.startswith(variation):
                return key
    return answer[0]

#def alphacharold(request):
    # if request.method == 'POST' and 'audio_file' in request.FILES:
    #     audio_file = request.FILES['audio_file']
    #     media_root = settings.MEDIA_ROOT
    #     if not os.path.exists(media_root):
    #         os.makedirs(media_root)
    #     audio_path = os.path.join(media_root, 'recording.wav')
    #     with open(audio_path, 'wb+') as destination:
    #         for chunk in audio_file.chunks():
    #             destination.write(chunk)
    #     answer = predict_alphabet(audio_path)
    #     correct_answer = chr(ord('a') + request.session.get('n_index', 1) - 1)
    #     correct = (answer == correct_answer)
    #     os.remove(audio_path)
    #     response = {
    #         "message": "Correct!" if correct else "Incorrect",
    #         "[DEBUG]": correct_answer,
    #         "recognized_text": answer,
    #     }
    #     return JsonResponse(response)
    # return JsonResponse({"message": "Invalid request"}, status=400)

def text_to_speech(request):
    text = request.GET.get('text', '')
    language = request.GET.get('lang', 'th')  # Default to Thai
    if text:
        tts = gTTS(text, lang=language)
        response = HttpResponse(content_type='audio/mpeg')
        tts.write_to_fp(response)
        response['Content-Disposition'] = 'inline; filename="speech.mp3"'
        return response
    return HttpResponse("No text provided.", status=400)

def alphachar(request):
    n = request.session.get('n_index', 1)
    answer = normalize_answer(correction_system())
    correct_answer = chr(ord('a') + n - 1)
    correct = (answer == correct_answer)
    if answer == correct_answer:
        correct = True
        response = {
            "message" : "Correct!",
            "recognized_text" : answer,
        }
    if not correct:
        response = {"message": "incorrect", "recognized_text" : answer}
    return JsonResponse(response)


def lower(request):
    return render(request, "sort.html")

def sort(request):
    return render(request, "sort.html")

def sorttryagain(request):
    return render(request, "Tryagain.html")

def sortcorrect(request):
    return render(request, "good.html")

def random(request):
    return render(request, "random.html")

def randomawe(request):
    return render(request, "randomawe.html")

def randomtry(request):
    return render(request, "randomtry.html")