from django.contrib.auth.models import User

def UA():
	user = User.objects.all()
	print(user)
