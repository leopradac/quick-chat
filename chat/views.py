from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def chat(request):
    return render(request, 'chat.html')
