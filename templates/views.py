# views.py
from django.shortcuts import render

def websocket_test(request):
    return render(request, 'websocket_test.html')
