from django.shortcuts import render,redirect

# Create your views here.

from .models import Photo
from .forms import UploadModelForm

def uploadFile(request):
    photos = Photo.objects.all()
    
    form = UploadModelForm()
    
    if request.method == "POST":
        
        form = UploadModelForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("/photos")
    
    
    context = {
        "photos":photos,
        "form":form
        }
    
    return render(request,"photos.html",locals())

def index(request):
    return render(request,"index.html")






