from django.shortcuts import render

# Create your views here.
def homescreen(request):
    return render(request, "home.html")

def basicbraille(request):
    return render(request, "basicbraille.html")

def main(request):
    return render(request, "Portals.html")

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