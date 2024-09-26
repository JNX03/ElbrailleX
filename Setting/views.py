from django.shortcuts import render

def tt(request):
    return render(request, 'TT.html')

def CM(request):
    return render(request, 'connnect.html')

def tran(request):
    return render(request, 'transalte.html')