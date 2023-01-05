from django.shortcuts import render

# Create your views here.

from .models import Message

def contact(request):
    
    msg = ""
    if "cuName" in request.POST:
        cuName = request.POST["cuName"]
        email = request.POST["email"]
        title = request.POST["title"]
        content = request.POST["content"]
        
        obj = Message.objects.create(name=cuName,email=email,subject=title,content=content)
        
        msg = "我們已收到您的訊息，將以最快的速度回覆您"
        
    return render(request,"contact.html",locals())
