"""SanskrutiFashionHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('', base, name='home'),
    path('men/', Men, name='men'),
    path('men1/<int:id>/', men1, name='men1'),
    path('men2/<int:id>/', men2, name='men2'),
    path('mens/<int:id>/', mens, name='mens'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('kids/', kids, name='kids'),
    path('register/', Register_m, name='register'),
    path('login/', Login, name='login'),
    path('cart/<int:id>/', cart, name='cart'),#link kaha he ye 
    path('show_cart/', show_cart, name='show_cart'),
    path('order/', order, name='order'),
    path('logout/', Logout, name='logout'),
    path('checkout/', checkout, name='checkout'),
    path('search/', Search, name='search'),
    path('plus/<int:id>/', plus, name='plus'),
    path('minus/<int:id>/', minus, name='minus'),
    path('remove/<int:id>/', remove, name='remove'),
    path('order/', order, name='order'),
    path('response/', response, name='response'),
    path('sub/', sub, name='sub'),
    path('faq/', faq, name='faq'),
    path('myorder/', myorder, name='myorder'),
    path('forpass/', forpass, name='forpass'),
    path('email_otp/', email_otp, name='email_otp'),
    path('password_match/', match_pass, name='password_match'),
    path('display/',display,name='display'),

    path('receipt/', receipt, name='receipt'),
    path('product_search/', product_search, name='product_search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
