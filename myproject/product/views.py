from django.shortcuts import render

from .models import Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def product(request):
    
    keyword = ""
    priceS = ""
    priceE = ""
    
    if "p" in request.GET:
         keyword = request.GET["p"]
         priceS = request.GET["priceS"]
         priceE = request.GET["priceE"]
         
         if (len(keyword) > 0 and len(priceS) == 0 and len(priceE) == 0):
             allgoods = Product.objects.filter(name__icontains = keyword).order_by("price")
             
         elif (len(keyword) == 0 and len(priceS) > 0 and len(priceE) > 0):
             allgoods = Product.objects.filter(price__gte=priceS,price__lte=priceE).order_by("price")
         
         elif (len(keyword) >0 and len(priceS) > 0 and len(priceE) > 0):
             allgoods = Product.objects.filter(name__icontains = keyword,price__gte=priceS,price__lte=priceE).order_by("price")
         
         elif (len(keyword) == 0 and len(priceS) > 0 and len(priceE) == 0):
             allgoods = Product.objects.filter(price__gte=priceS).order_by("price")
             
         elif (len(keyword) == 0 and len(priceS) == 0 and len(priceE) > 0):
             allgoods = Product.objects.filter(price__lte=priceE).order_by("price")
             
         else:
             allgoods = Product.objects.all().order_by("-id")
    else:
        allgoods = Product.objects.all().order_by("-id")
        
    
    paginator = Paginator(allgoods,12)
    page = request.GET.get("page")
    
    try:
        allgoods = paginator.page(page)
    except PageNotAnInteger:
        allgoods = paginator.page(1)
    except EmptyPage:
        allgoods = paginator.page(paginator.num_pages)
    
    
    
    return render(request,"product.html",locals())
