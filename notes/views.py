from django.shortcuts import render

# Create your views here.
def index(request):
    context={}
    return render(request,'index.html',context)

def download_section(request):
    context={}
    return render(request,'download_section.html',context)

