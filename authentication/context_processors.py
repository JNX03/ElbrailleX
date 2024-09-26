from django.conf import settings

def youtube_video(request):
    return {
        'YOUTUBE_VIDEO_ID': settings.YOUTUBE_VIDEO_ID,
    }