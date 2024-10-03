from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from .braille_translation import translate_to_braille
import PyPDF2  # For handling PDFs
from docx import Document  # Correct import for python-docx
from odf import text, teletype
from odf.opendocument import load
from django.core.files.storage import FileSystemStorage

def success(request):
    return render(request, 'success.html')

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()

            file_path = document.file.path
            extracted_text = ''

            # Check the file extension to determine the handling method
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    for page in range(len(reader.pages)):
                        extracted_text += reader.pages[page].extract_text()

            elif file_path.endswith('.docx'):
                doc = Document(file_path)  # Use Document from python-docx
                for paragraph in doc.paragraphs:
                    extracted_text += paragraph.text + '\n'
            
            elif file_path.endswith('.odt'):
                odt_doc = load(file_path)
                for element in odt_doc.getElementsByType(text.P):
                    extracted_text += teletype.extractText(element) + '\n'
            
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    extracted_text = file.read()
            
            else:
                # Handle unsupported file types
                return render(request, 'upload.html', {
                    'form': form,
                    'error_message': 'Unsupported file type.'
                })

            # Translate the extracted text to Braille
            braille_text = translate_to_braille(extracted_text)
            document.braille_text = braille_text
            document.save()

            return render(request, 'display.html', {'braille_text': braille_text})
    else:
        form = DocumentForm()

    return render(request, 'upload.html', {'form': form})
