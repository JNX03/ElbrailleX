from django.shortcuts import render
import random
import string
import requests

def random_letter_view(request):
    random_letter = random.choice(string.ascii_lowercase)
    generated_string = generate_random_string(random_letter)
    
    firebase_url = 'https://brailleproject-8091a-default-rtdb.asia-southeast1.firebasedatabase.app/BDID/getfunc.json'
    
    update_firebase(firebase_url, generated_string)
    
    return render(request, "game.html", {'letter': random_letter, 'generated_string': generated_string})

def generate_random_string(must_include):
    other_letters = random.choices(string.ascii_lowercase.replace(must_include, ''), k=4)
    combined = [must_include] + other_letters
    random.shuffle(combined)
    return ''.join(combined)

def update_firebase(url, data):
    requests.put(url, json={'value': data})

def upper(request):
    return render(request, "uppper.html")

def lower(request):
    return render(request, "small.html")

def short(request):
    return render(request, "short.html")

def math2(request):
    return render(request, "math2.html")
def sym1(request):
    return render(request, "sym.html")