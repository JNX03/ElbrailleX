from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .braille_translation import translate_to_braille
import PyPDF2
from docx import Document as DocxDocument
from odf import text, teletype
from odf.opendocument import load

def success(request):
    return render(request, 'success.html')

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            file_path = document.file.path
            extracted_text = ''

            try:
                if file_path.endswith('.pdf'):
                    with open(file_path, 'rb') as pdf_file:
                        reader = PyPDF2.PdfReader(pdf_file)
                        for page in range(len(reader.pages)):
                            page_text = reader.pages[page].extract_text()
                            if page_text:
                                extracted_text += page_text

                elif file_path.endswith('.docx'):
                    doc = DocxDocument(file_path)
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
                    return render(request, 'file.html', {
                        'form': form,
                        'error_message': 'Unsupported file type.'
                    })
                
                if not extracted_text.strip():
                    return render(request, 'file.html', {
                        'form': form,
                        'error_message': 'Failed to extract text from the file.'
                    })

                braille_text = translate_to_braille(extracted_text)
                document.braille_text = braille_text
                document.save()

                return render(request, 'display.html', {'braille_text': braille_text})
            
            except Exception as e:
                return render(request, 'file.html', {
                    'form': form,
                    'error_message': f'An error occurred: {str(e)}'
                })

    else:
        form = DocumentForm()

    return render(request, 'file.html', {'form': form})
