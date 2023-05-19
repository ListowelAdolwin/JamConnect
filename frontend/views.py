from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request, *args, **kwargs):
    #return HttpResponse("Yaayyy, You worked!")
    return render(request, 'frontend/index.html')
