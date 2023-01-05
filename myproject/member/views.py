from django.shortcuts import render

import hashlib

from .models import Member
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

def login(request):
    msg = ""
    if "email" in request.POST:
        email = request.POST["email"]
        password = request.POST["pwd"]
        password = hashlib.sha3_256(password.encode("utf-8")).hexdigest()

        obj = Member.objects.filter(email=email,password=password).count()
        
        if obj > 0:
            request.session["myMail"] = email
            request.session["isAlive"] = True
            
            return HttpResponseRedirect("/member")
        
        else:
            msg = "帳號或密碼錯誤, 請重新輸入"
            
            return render(request,"login.html",locals())
    
    else:
        if "myMail" in request.session and "isAlive" in request.session:
            return HttpResponseRedirect("/member")
        
        else:
            return render(request,"login.html",locals())
            
        
def logout(request):
    del request.session["isAlive"]
    del request.session["myMail"]
    
    return HttpResponseRedirect("/login")
    

def register(request):
    msg = ""
    
    if "username" in request.POST:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["pwd"]
        sex = request.POST["sex"]
        birthday = request.POST["birthday"]
        address = request.POST["address"]
        
        #密碼加密
        password = hashlib.sha3_256(password.encode("utf-8")).hexdigest()
        
        #確認Email是否重複
        obj = Member.objects.filter(email=email).count()
        
        if obj == 0:
            Member.objects.create(name=username,email=email,sex=sex,birthday=birthday,password=password,address=address)
            msg = "恭喜您，已完成註冊！"
            
            return render(request,"login.html",locals())
            
        else:
            msg = "此Email已存在，請換一個Email註冊"
    
    

    return render(request,"register.html",locals())

def manage(request):
    if "myMail" in request.session and "isAlive" in request.session:
        
        msg = ""
        
        if "oldpwd" in request.POST:
            oldpwd = request.POST["oldpwd"]
            newpwd = request.POST["newpwd"]
            email = request.session["myMail"]
            
            oldpwd = hashlib.sha3_256(oldpwd.encode("utf-8")).hexdigest()
            newpwd = hashlib.sha3_256(newpwd.encode("utf-8")).hexdigest()
            
            obj = Member.objects.filter(email=email,password=oldpwd).count()
            if obj > 0:
                user = Member.objects.get(email=email)
                user.password = newpwd
                user.save()
                msg = "密碼變更完成"
            else:
                msg = "舊密碼不正確，請重新輸入"
                
        
        return render(request,"manage.html",locals())
    
    else:
        return HttpResponseRedirect("/login")










