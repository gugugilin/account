from django.shortcuts import render
from django.contrib.auth.models import User,Permission
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth  # 別忘了import auth
from django.views.decorators.csrf import csrf_exempt #我們import的 :D
from .models import *
import re

# Create your views here.

def SecurityCheck(name,password1,password2):
	print("SecurityCheck")

	if not ((len(name)>=1 and len(name)<=150) and (len(password1)>=8 and len(password1)<=300)):
		print("length")
		return False,None

	if password1!=password2:
		print("password not eq")
		return False,None
	
	c = name[0]
	if not((c>="a" and c<="z") or (c>="A" and c<="Z")):
		print("name is not valid")
		return False,None

	for c in name:
		if not((c>="a" and c<="z") or (c>="A" and c<="Z") or (c>="0" and c<="9")):
			print("name is not valid")
			return False,None



	Digit = False
	Alphabet = False


	for c in password1:
		if((c>="0" and c<="9")):
			Digit = True
		elif((c>="a" and c<="z") or (c>="A" and c<="Z")):
			Alphabet = True
		else:
			print("password is not valid")
			return False,None

	user = auth.authenticate(username=name, password=password1)
	if user!=None:
		print("had register")
		return True,user
	else:
		user_list=User.objects.filter(username=name)
		if len(user_list)==0:
			print("user_list")
			return (Alphabet and Digit),None
		else:
			print("Password Error :3")
			return False,user_list[0]

	return (Alphabet and Digit),user

def isfloat(str):
    try: 
        float(str)
    except: 
        return False
    return True

@csrf_exempt #繞過防護機制
def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password1')
		print("POST")
		
		try:
			Valid,user = SecurityCheck(username,password,request.POST.get('password2'))
			if Valid:
				print("Valid: ",user)
				if user==None:
					form = UserCreationForm(request.POST)
					user = form.save()
				perm = Permission.objects.get(codename='can_account')
				user.user_permissions.add(perm)
				user.save()
				Account.objects.create(author = user)
				return render(request,'Account_HTML/login.html',{})
			else:
				print("Else_Not_Valid",user)
		except Exception as e:
			print(e)
	else:
		print("ELSE_Method")

	return render(request,'Account_HTML/register.html',{})

@csrf_exempt
def myaccount(request):
	print("myaccount")
	print(request.user.username)
	print(request.user.has_perm('account.can_account'))
	datas = []
	try:
		if len(Account.objects.filter(author=request.user))==0:
			return render(request,'Account_HTML/account.html',{'datas':[],'balance':0})

		if request.user.is_authenticated and request.user.has_perm('account.can_account'):
			datas = Detail.objects.filter(author = request.user).order_by('-id')
		else:
			return render(request,'Account_HTML/account.html',{'datas':datas,'balance':0})

		user = Account.objects.get(author=request.user)

		if(request.POST.get('Enter')):
			item = request.POST.get('item')
			item_len = len(item)
			if item_len>0 and item_len<50 and isfloat(request.POST.get('cost')):
				temp = re.match("[a-zA-Z0-9]+",item)
				if not(temp!=None and ((temp.span()[1] - temp.span()[0])==item_len)):
					return render(request,'Account_HTML/account.html',{'datas':datas,'balance':user.balance})
					Detail.objects.create(author = request.user,item = request.POST.get('item'),cost = int(request.POST.get('cost')))		
					user.balance -= float(request.POST.get('cost'))
					user.save()
				balance = user.balance
		elif(request.POST.get('DeleteAll')):
			datas = Detail.objects.filter(author = request.user).order_by('-id')
			datas.delete()
			user.balance = 0
			user.save()
		elif(request.POST.get('Delete')):
			print("Delete item")
			detail_item = Detail.objects.get(id = request.POST.get('myid'))
			user.balance += float(detail_item.cost)
			user.save()
			detail_item.delete()
		else:
			print("Error")
		balance = user.balance
	except Exception as e:
		print(e)
	return render(request,'Account_HTML/account.html',{'datas':datas,'balance':balance,'username':user.author.username})

@csrf_exempt #繞過防護機制
def login_pass(request):
	uname = request.POST.get('uname')
	psw = request.POST.get('psw')
	try:
		user = auth.authenticate(username=uname, password=psw)
		print("test: ",uname)
	except:
		user=None
	if user is not None and user.is_active:
		auth.login(request,user)
		return render(request,'Account_HTML/pass.html',{})
	else:
		return render(request,'Account_HTML/login.html',{})

def login(request):
	return render(request,'Account_HTML/login.html',{})

def post_list(request):
	return render(request,'Account_HTML/account.html',{})
