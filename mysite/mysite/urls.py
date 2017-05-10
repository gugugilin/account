from django.conf.urls import url,include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^blog/', include('blog.urls')),
	url(r'^account/',include('account.urls')),
	url(r'.*',include('error.urls'))
]
