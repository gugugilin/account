from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth  # 別忘了import auth
from django.views.decorators.csrf import csrf_exempt #我們import的 :D

# Create your views here.

@csrf_exempt #繞過防護機制
def register(request):
	if request.method == 'POST':
		print("POST")
		form = UserCreationForm(request.POST)
		if form.is_valid():
			print("VALID")
			user = form.save()
			return render(request,'blog_HTML/login.html',{})
	else:
		print("ELSE")
		form = UserCreationForm()
	return render(request,'blog_HTML/register.html',{})

def pass_img(request):
	img_name=request.POST.get('imgname')
	print(img_name)
	return render(request,'blog_PIC/'+img_name)

@csrf_exempt #繞過防護機制
def login_pass(request):
	print(request)
	uname = request.POST.get('uname')
	psw = request.POST.get('psw')
	user = auth.authenticate(username=uname, password=psw)
	print("test: ",user)
	if user is not None and user.is_active:
		auth.login(request,user)
		users = User.objects.all()
		return render(request,'blog_HTML/post_list.html',{'users':users})
	else:
		return render(request,'blog_HTML/login.html',{})

	# if( not (uname==None or psw==None) ):
	# 	user = User.objects.create_user(uname,psw)
	# 	user.save()

	# return render(request,'blog_HTML/post_list.html',{})

def login(request):
	return render(request,'blog_HTML/login.html',{})

def post_list(request):
	return render(request,'blog_HTML/post_list.html',{})