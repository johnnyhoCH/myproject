from django.shortcuts import render


from .models import Player
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def player(request):
    
    data = Player.objects.all().order_by("id")
    
    paginator = Paginator(data,3)
    
    page = request.GET.get("page")
    
    try:
        pagedata = paginator.page(page)
        
    except PageNotAnInteger:
        pagedata = paginator.page(1)
        
    except EmptyPage:
        pagedata = paginator.page(paginator.num_pages)
    
    alldata = {"playerlist":pagedata}
    
    return render(request,"player.html",alldata)
