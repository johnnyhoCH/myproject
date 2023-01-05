from django.shortcuts import render

# Create your views here.





def aboutus(request):
    
    return render(request,"aboutus.html")


def pics(request):
    
    return render(request,"pics.html")
