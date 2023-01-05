"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from player.views import player
from product.views import product
from cart.views import cart, add_to_cart, cart_order,cart_ok,cart_order_check,myorder,ECPayCredit

from member.views import login, logout, register, manage
from photos.views import uploadFile, index

from django.conf import settings
from django.conf.urls.static import static

from message.views import contact
from aboutus.views import aboutus, pics 

from news.views import news

urlpatterns = [
    path("admin/", admin.site.urls),
    path("player/", player),
    path("product/",product),
    path("cart/",cart),
    path("add_to_cart/<str:ctype>/",add_to_cart),
    path("add_to_cart/<str:ctype>/<int:productid>/",add_to_cart),
    path("cart_order/",cart_order),
    path("cart_ok/",cart_ok),
    path("cart_order_check/",cart_order_check),
    path("login/",login),
    path("logout/",logout),
    path("register/",register),
    path("member/",manage),
    path("myorder/",myorder),
    path("creditcard/",ECPayCredit),
    path("photos/",uploadFile),
    path("",index),
    path("contact/",contact),
    path("aboutus/",aboutus),
    path("pics/",pics),
    path("news/",news)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)




