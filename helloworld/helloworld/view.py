from django.http import HttpResponse

from django.shortcuts import render


def helloTemplates(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)


def hello(request):
    return HttpResponse("Hello World!")
