from . import views
from django.conf.urls import url, include

app_name = 'index'
urlpatterns = [
    url(r'^$', views.about_us, name='about_us'),
]
