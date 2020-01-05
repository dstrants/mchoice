from django.conf.urls import url, include
from django.contrib import admin
from tests import urls as test_urls

urlpatterns = [
    url('admin/', admin.site.urls),
    url('', include(test_urls)),
    url('auth/', include('django.contrib.auth.urls')),
]
