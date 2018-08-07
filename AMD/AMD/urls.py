from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from AMD.music import views


urlpatterns = [
    url(r'^$', views.home, name='home'), #포스팅 목록
    url(r'converter', views.converter, name='converter'), #포스팅 목록
    url(r'play', views.play, name='play'), #포스팅 목록
    url(r'^$', views.record, name='record'), #포스팅 목록
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
