from django.shortcuts import render

# Create your views here.

def smallalphabetlearning(request, n):
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
    letter = chr(ord('a')-1+n)
    context = {
        "n": n,
        "n_prev": n-1,
        "n_next": n+1,
        "letter": letter,
        "braille_pattern": braille_patterns.get(letter, [0, 0, 0, 0, 0, 0])
    }
    if n == 1:
        return render(request, "smallalphabetlearning1.html", context)
    elif n == 26:
        return render(request, "smallalphabetlearning2.html", context)
    return render(request, "smallalphabetlearning.html", context)

def bigalphabetlearning(request, n):
    braille_patterns = {
        'A': [1, 0, 0, 0, 0, 0],
        'B': [1, 1, 0, 0, 0, 0],
        'C': [1, 0, 0, 1, 0, 0],
        'D': [1, 0, 0, 1, 1, 0],
        'E': [1, 0, 0, 0, 1, 0],
        'F': [1, 1, 0, 1, 0, 0],
        'G': [1, 1, 0, 1, 1, 0],
        'H': [1, 1, 0, 0, 1, 0],
        'I': [0, 1, 0, 1, 0, 0],
        'J': [0, 1, 0, 1, 1, 0],
        'K': [1, 0, 1, 0, 0, 0],
        'L': [1, 1, 1, 0, 0, 0],
        'M': [1, 0, 1, 1, 0, 0],
        'N': [1, 0, 1, 1, 1, 0],
        'O': [1, 0, 1, 0, 1, 0],
        'P': [1, 1, 1, 1, 0, 0],
        'Q': [1, 1, 1, 1, 1, 0],
        'R': [1, 1, 1, 0, 1, 0],
        'S': [0, 1, 1, 1, 0, 0],
        'T': [0, 1, 1, 1, 1, 0],
        'U': [1, 0, 1, 0, 0, 1],
        'V': [1, 1, 1, 0, 0, 1],
        'W': [0, 1, 0, 1, 1, 1],
        'X': [1, 0, 1, 1, 0, 1],
        'Y': [1, 0, 1, 1, 1, 1],
        'Z': [1, 0, 1, 0, 1, 1],
    }
    letter = chr(ord('A')-1+n)
    context = {
        "n": n,
        "n_prev": n-1,
        "n_next": n+1,
        "letter": letter,
        "braille_pattern": braille_patterns.get(letter, [0, 0, 0, 0, 0, 0])
    }
    if n == 1:
        return render(request, "bigalphabetlearning1.html", context)
    elif n == 26:
        return render(request, "bigalphabetlearning2.html", context)
    return render(request, "bigalphabetlearning.html", context)

def numberlearning(request, n):
    braille_patterns = {
        '1': [1, 0, 0, 0, 0, 0],
        '2': [1, 1, 0, 0, 0, 0],
        '3': [1, 0, 0, 1, 0, 0],
        '4': [1, 0, 0, 1, 1, 0],
        '5': [1, 0, 0, 0, 1, 0],
        '6': [1, 1, 0, 1, 0, 0],
        '7': [1, 1, 0, 1, 1, 0],
        '8': [1, 1, 0, 0, 1, 0],
        '9': [0, 1, 0, 1, 0, 0],
        '0': [0, 1, 0, 1, 1, 0],
    }
    letter = chr(ord('1')-1+n)
    context = {
        "n": n,
        "n_prev": n-1,
        "n_next": n+1,
        "letter": letter,
        "braille_pattern": braille_patterns.get(letter, [0, 0, 0, 0, 0, 0])
    }
    if n == 1:
        return render(request, "numberlearning1.html", context)
    elif n == 10:
        return render(request, "numberlearning2.html", context)
    return render(request, "numberlearning.html", context)

def shorten1(request):
    return render(request, "shorten1.html")
def shorten2(request):
    return render(request, "shorten2.html")
def mathlearning(request):
    return render(request, "mathlearning1.html")
def math1(request):
    return render(request, "math1.html")
def math2(request):
    return render(request, "math2.html")
def math3(request):
    return render(request, "math3.html")

def op1(request):
    return render(request, "op1.html")
def op2(request):
    return render(request, "op2.html")

def opc1(request):
    return render(request, "opc1.html")
def opc2(request):
    return render(request, "opc2.html")

def sym1(request):
    return render(request, "Symbol1.html")

def sym2(request):
    return render(request, "Symbol2.html")