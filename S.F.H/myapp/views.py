from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.core import serializers
from . import Checksum
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .utils import VerifyPaytmResponse
import requests
from django.core.mail import EmailMessage

# Create your views here.
def cart(request,id):
	con = {}
	print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")

	if 'user' in request.session:
		user = request.session['user']
		us = Register.objects.get(useremail=user)
		product = Product.objects.get(pk=id)
		print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",product)

		cart_exists = Cart.objects.filter(user=us,product__p_name=product.p_name,status=False)
		qty = 1
		if cart_exists:
			pass
		else:
			Cart(user=us,product=product,qauntity=qty,total=product.p_price).save()

		con['cart']=Cart.objects.filter(user__useremail=user,status=False)
	
	return render(request,'cart.html',con)

def show_cart(request):
	con={}
	if 'user' in request.session:
		user =  request.session['user']
		con['cart']=Cart.objects.filter(user__useremail=user,status=False)

		
		cart =  Cart.objects.filter(user__useremail=user,status=False)
		total,qty=0,0
		for c in cart:
			total +=c.total
			qty+=c.qauntity
		con['total']=total
		con['qty']=qty
		con['subtotal']=total+70


		return render(request,'cart.html',con)
	else:
		return redirect('login')

def	order(request):
	con={}
	if 'user' in request.session:
		user =  request.session['user']
		con['cart']=Cart.objects.filter(user__useremail=user,status=False)

		
		cart =  Cart.objects.filter(user__useremail=user,status=False)
		total,qty=0,0
		for c in cart:
			total +=c.total
			qty+=c.qauntity
		con['total']=total
		con['qty']=qty
		con['subtotal']=total+70
		
		

	
	if request.method == "POST":
		us = request.session['user']
		user = Register.objects.get(useremail=us)
		
		print(cart)
		data = serializers.serialize('json', cart)
		product=data
		fullname = request.POST['name']
		mobileno = request.POST['mobileno']
		landmark = request.POST['landmark']
		town = request.POST['town']
		state = request.POST['state']
		addresstype = request.POST['addresstype']
		payment = request.POST['paymet']
		import random

		o_id = random.randint(00000,99999)

		if payment == "online":
			order_id = Checksum.__id_generator__()
			tt = str(con['subtotal'])
			bill_amount = tt
			data_dict = {
			    'MID': settings.PAYTM_MERCHANT_ID,
			    'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
			    'WEBSITE': settings.PAYTM_WEBSITE,
			    'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
			    'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
			    'MOBILE_NO': mobileno,
			    'EMAIL': user.useremail,
			    'CUST_ID': str(o_id),
			    'ORDER_ID':order_id,
			    'TXN_AMOUNT': bill_amount,
			} # This data should ideally come from database
			data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
			context = {
			    'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
			    'comany_name': settings.PAYTM_COMPANY_NAME,
			    'data_dict': data_dict
			}
			cart = Cart.objects.filter(user=user)
			for c  in cart:
			
				order = Order(user=user,cart_id=c.id,fullname=fullname,mobileno=mobileno,landmark=landmark,town=town,state=state,addresstype=addresstype)
				c.status =True
				c.save()
				order.save()
			
			return render(request, 'payment.html', context)

	 
		print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
	return render(request,'inn.html')

@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        return render(request,"receipt.html",{"response":resp})
    else:
        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h>")

def base(request):
	print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

		
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	print(wcat2,"KKKKKKKKKKKKKKKKKKKKKKKKKKK")
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	return render(request,'inn.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})


def home(request):
	
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_cub_name='Western wear')
	print(wcat1,"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSKKKKKKKKKKKKKKKKKKKKKKKKKKK")
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	print(wcat2,"KKKKKKKKKKKKKKKKKKKKKKKKKKK")
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection') 
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	ks = Product.objects.filter(cat_sub_two__id=33)

	
	return render(request,'inn.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def Men(request):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_cub_name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	print(wcat2,"KKKKKKKKKKKKKKKKKKKKKKKKKKK")
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	return render(request,'men.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def men1(request,id):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	print(wcat2,"KKKKKKKKKKKKKKKKKKKKKKKKKKK")
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	tm = Product.objects.filter(cat_sub_two__id=id) 
	se = Product.objects.filter(p_name='icontains')
	
	return render(request,'catm.html',{"se":se,"tm":tm,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def men2(request,id):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	tm = Product.objects.filter(cat_sub_two__id=id)
	print(tm,"pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")


	return render(request,'catm2.html',{"tm":tm,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def mens(request,id):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	print(wcat2,"KKKKKKKKKKKKKKKKKKKKKKKKKKK")
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	ms2 = Product.objects.filter(pk=id)
	ms2 = Product.objects.filter(pk=id)
	tm = Product.objects.filter(cat_sub_two__cat_sub__cat__id=id)
	
	return render(request,'mens.html',{"tm":tm,"ms2":ms2,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def receipt(request):
	return render(request,'receipt.html')

def about(request):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	return render(request,'about.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def contact(request):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	return render(request,'contact.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def kids(request):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	return render(request,'Kids.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def Search(request):
	return render(request,'sea.html')



def faq(request):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	return render(request,'faq.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

def myorder(request):
	if "user" in request.session:
		mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
		mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
		wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
		wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
		kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
		kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
		kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
		# wcat = Subcategory.objects.filter(cat__name='Women')
		data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
		data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
		m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
		w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
		k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
		us=request.session['user']
		data=Order.objects.filter(user__useremail=us)


		return render(request,'myorder.html',{"order":data,"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})

			
		# return render(request,'myorder.html',{"menh":m1,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2})
	else:
		return redirect("login")


def checkout(request):
	
	con={}
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
		# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	m1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=1)
	w1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=2)
	k1 = Product.objects.filter(cat_sub_two__cat_sub__cat__id=3)
	# con["mcat"]
	if 'user' in request.session:
		user =  request.session['user']
		con['cart']=Cart.objects.filter(user__useremail=user,status=False)

		cart =  Cart.objects.filter(user__useremail=user,status=False)
		total,qty=0,0
		for c in cart:
			total +=c.total
			qty+=c.qauntity
		con['total']=total
		con['qty']=qty
		con['subtotal']=total+70
	
		return render(request,'checkout.html',con)

def Register_m(request):
	msg ={}
	if request.method == "POST":
		uname = request.POST['uname']
		uemail = request.POST['uemail']
		upassword = request.POST['upassword']
		umobileno = request.POST['umobileno']
		uconfirmPassword = request.POST['uconfirmPassword']
		#selector = request.POST['selector']
		if (upassword == uconfirmPassword):
			msg['msg']="Data save"
			user = Register(username=uname,useremail=uemail,userpassword=upassword,usermobileno=umobileno)
			user.save()
		else:
			msg['msg']="Password does not match"
			
	return render(request,'register.html',msg)

def Login(request):
	if request.method == "POST":
		em = request.POST['email']
		lpwd = request.POST['lpwd']
		user = Register.objects.get(useremail=em)
		if user.userpassword==lpwd:
			request.session['user']=em
			return redirect("home")
	return render(request,'log.html')

def Logout(request):
	del request.session['user']
	return redirect('login')


def plus(request,id):
	cart =  Cart.objects.get(id=id)
	total = cart.product.p_price
	cart.qauntity+=1
	cart.total = total*cart.qauntity
	
	cart.save()
	return redirect('show_cart')

	# return render(request,'cart.html')
	
	
def minus(request,id):
	cart =  Cart.objects.get(id=id)
	total = cart.product.p_price
	cart.qauntity-=1
	cart.total = total*cart.qauntity
	cart.save()
	return redirect('show_cart')

	
def remove(request,id):
	cart =  Cart.objects.get(id=id)
	cart.delete()
	return redirect('show_cart')

	# return render(request,'cart.html')
	
def sub(request):
	if request.method =="POST":
		email =  request.POST['email']
		Subscribe(email=email).save()
		return redirect('home')


def product_search(request):
	mcat = Subcategory_two.objects.filter(cat_sub__name='Topwear')
	mcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Festive wear')
	wcat = Subcategory_two.objects.filter(cat_sub__name='Western wear')
	wcat2 = Subcategory_two.objects.filter(cat_sub__name='Indian & Fussion wear')
	kcat = Subcategory_two.objects.filter(cat_sub__name='Boys')
	kcat2 = Subcategory_two.objects.filter(cat_sub__name='Girls')
	kscat = Subcategory_two.objects.filter(cat_sub__name='Collection')
	# wcat = Subcategory.objects.filter(cat__name='Women')
	data = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Men')
	data2 = Product.objects.filter(cat_sub_two__cat_sub__cat__name='Women')
	tm = ''
	if request.method == "POST":
		search_p = request.POST['product_search']
		tm = Product.objects.filter(p_name__icontains=search_p)

	
	return render(request,'catm.html',{"tm":tm,"data":data,"data2":data2,"cat": mcat,"cat2":mcat2,"wca":wcat,"wca2":wcat2,"kca":kcat,"kca2":kcat2,"kca3":kscat})



	#foragate 
import random


def forpass(request):
	
	if request.method =="POST":
		email_id = request.POST['email']
		otp = random.randint(000000,999999)
		user = Register.objects.get(useremail=email_id)
		if user is not None :
			email1 = EmailMessage(
			'OTP Verification',
			f'Your OTP : {otp}',
			'chandekarsanjana1020@gmail.com',
			[email_id],)
			request.session['otp']=otp
			request.session['useremail']=user.useremail
			email1.send()
			return redirect('email_otp')
		else:
			error = "User not found"
			render(request,'forpass.html',{"error":error})
	return render(request,'forpass.html')
	
	
def email_otp(request):
	in_otp = request.session['otp']
	print(type(in_otp),'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')

	if request.method =="POST":
		otp = request.POST['m_otp']
		print(type(in_otp),'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
		print(type(otp),'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')


		if str(in_otp) == str(otp):
			print(type(otp),'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
			return redirect('password_match')
		else:
			print("otp not match")
			return redirect("email_otp")
	else:
		return render(request,'otp.html')



def match_pass(request):

	if 'useremail' in request.session:
		email = request.session['useremail']
		user = Register.objects.get(useremail=email)
		if request.method == "POST":
			pass1 = request.POST['pass']
			pass12 = request.POST['pass1']
			print( 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
			if pass1 == pass12:
				print('5555555555555555555555555555555555555555555555555555555')
				user.userpassword= pass12
				user.save()
				return redirect('login')
			else:
				print("pass and pass1 does not match")
				return redirect('password_match')
		else:
			return render(request ,"password_match.html")
	else:
		return redirect('forpass')


	user = Register.objects.get(useremail=request.session['user'])
	
	return render(request,'password_match.html')

def display(request):
	us=request.session['user']
	data=Order.objects.filter(user__useremail=us)
	print(data,"HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
	return render(request,'myorder.html',{'data':data})

