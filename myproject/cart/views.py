from django.shortcuts import render,redirect

from django.http import HttpResponseRedirect

from cart import models

from product.models import Product

from django.utils.html import format_html

#崁入ECPay SDK
import os
basedir = os.path.dirname(__file__)
file = os.path.join(basedir,"ecpay_payment_sdk.py")
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime


# Create your views here.


cartlist = list()
custom_name = ""
custom_phone = ""
custom_address = ""
custom_email = ""

orderTotal = 0
goodsTitle = list()

def add_to_cart(request,ctype=None,productid=None):
    global cartlist
    
    if ctype == "add":
        product = Product.objects.get(id=productid)
        flag = True
        
        for unit in cartlist:
            if product.name == unit[0]:
                unit[2] = str(int(unit[2]) + 1)
                unit[3] = str(int(unit[3])+ product.price)
                flag = False
                break
        if flag:
            templist = list()
            templist.append(product.name)
            templist.append(str(product.price))
            templist.append("1")
            templist.append(str(product.price))
            cartlist.append(templist)
        
        
        request.session["cartlist"] = cartlist
        
        return redirect("/cart/")
    
    elif ctype == "update":
        n = 0
        for unit in cartlist:
            
            amount = request.POST.get("qty" + str(n),"1")
            
            if len(amount) == 0:
                amount = "1"
            if int(amount) <= 0:
                amount = "1"
                
            unit[2] = amount
            
            unit[3] = str(int(unit[1]) * int(unit[2]))
            
            n += 1
        
        request.session["cartlist"] = cartlist
        return redirect("/cart/")
    
    elif ctype == "empty":
        cartlist = list()
        request.session["cartlist"] = cartlist
        return redirect("/cart/")
    
    elif ctype == "remove":
        del cartlist[int(productid)]
        request.session["cartlist"] = cartlist
        return redirect("/cart/")
    

def cart(request):
    global cartlist
    allcart = cartlist
    total = 0
    
    for unit in cartlist:
        total += int(unit[3])
    
    grandtotal = total + 100 #shipping
    return render(request,"cart.html",locals())

def cart_order(request): #結帳
    
    if "myMail" in request.session and "isAlive" in request.session:
        global cartlist,custom_name,custom_phone,custom_address,custom_email
        
        total = 0
        allcart = cartlist
        for unit in cartlist:
            total += int(unit[3])
        grandtotal = total + 100
        
        name = custom_name
        phone = custom_phone
        email = request.session["myMail"]
        address = custom_address
        
        return render(request,"cart_order.html",locals())
    
    else:
        return render(request,"login.html",locals())

def cart_ok(request):       #確認資料並送出, 寫入資料庫
    global cartlist, custom_address,custom_email,custom_name,custom_phone
    
    global orderTotal, goodsTitle
    
    total = 0
    for unit in cartlist:
        total += int(unit[3])
        
    grandtotal = total + 100 
    orderTotal = grandtotal
    
    custom_name = request.POST.get("cuName","")
    custom_phone = request.POST.get("cuPhone","")
    custom_address = request.POST.get("cuAddress","")
    custom_email = request.POST.get("cuEmail","")
    pay_type = request.POST.get("payType","")
    
    unitorder = models.OrdersModel.objects.create(subtotal=total,shipping=100,grandtotal=grandtotal,custom_name=custom_name,custom_phone=custom_phone,custom_address=custom_address,custom_email=custom_email,pay_type=pay_type)

    for unit in cartlist:
        goodsTitle.append(unit[0])
        total = int(unit[1])*int(unit[2])
        unitdetail = models.DetailModel.objects.create(dorder=unitorder,product_name=unit[0],unitprice=unit[1],quantity=unit[2],dtotal=total)


    orderid = unitorder.id
    name = unitorder.custom_name
    email = unitorder.custom_email
    
    cartlist = list()       #清空購物車
    request.session["cartlist"] = cartlist
    
    if pay_type == "信用卡":
        return HttpResponseRedirect("/creditcard",locals())
    else:
        return render(request,"cart_ok.html",locals())
    

def cart_order_check(request):  #訂單完成供查詢用
    orderid = request.GET.get("orderid","")
    custom_email = request.GET.get("custom_email","")
    
    if orderid == "" and custom_email == "":
        nosearch = 1
    else:
        order = models.OrdersModel.objects.filter(id=orderid).first()
        
        if order == None:
            notfound = 1
        else:
            details = models.DetailModel.objects.filter(dorder=order)
            
    return render(request,"cart_order_check.html",locals())

def myorder(request):
    
    if "myMail" in request.session and "isAlive" in request.session:
        email = request.session["myMail"]
        
        order = models.OrdersModel.objects.filter(custom_email=email)
        
        return render(request,"myorder.html",locals())
    
    else:
        msg = "請先登入會員"
        return render(request,"login.html",locals())
    
def ECPayCredit(request):
    
    global goodsTitle
    title = ""
    for i in goodsTitle:
        title += i +"#"
        
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal,
        'TradeDesc': '訂單測試',
        'ItemName': title,
        'ReturnURL': 'https://www.google.com.tw/',
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.google.com.tw/',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.google.com.tw/',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html)
        return render(request,"paycredit.html",locals())
    except Exception as error:
        print('An exception happened: ' + str(error))








    



