from django.shortcuts import render

def index(request):
    pageTitle = 'SMM'
    pageDescription = 'SMM'
    return render(request, 'front/index.html', locals())
