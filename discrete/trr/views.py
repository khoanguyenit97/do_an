from django.shortcuts import render
from django.http import HttpResponse, Http404
#from .controllers import TreeController, IndexController


# Create your views here.
def index(request):
    return render(request, 'index.html')
    