from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload

def tt(request):
    return render(request, 'TT.html')

def CM(request):
    return render(request, 'connnect.html')

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save the file and get the model instance
            # Redirect to success view with file URL
            return render(request, 'upload_success.html', {'file_url': uploaded_file.file.url})
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def file_list(request):
    files = FileUpload.objects.all()  # Retrieve all uploaded files
    return render(request, 'file_list.html', {'files': files})

def upload_success(request):
    return render(request, 'upload_success.html')