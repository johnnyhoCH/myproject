from django.shortcuts import render

# Create your views here.

from .models import News

def news(request):
    
    keyword = ""
    
    if 'p' in request.GET:
    
        keyword = request.GET['p']
        
        if len(keyword) > 0:
            data = News.objects.filter(title__icontains = keyword).order_by("-create_date")
        else:
            data = News.objects.all().order_by("-create_date")
    else:
        
        data = News.objects.all().order_by("-create_date")
    
    return render(request,"news.html",locals())
