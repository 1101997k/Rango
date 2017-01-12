from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage' : "testing"}

    return render(request, 'rango/index.html', context=context_dict)
def about(request):
    return HttpResponse("<h1>Rango says about page!</h1><br/> <a href='/rango/'>Home</a>")
