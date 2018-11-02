from django.conf.urls import url
from . import views

app_name = 'Application'
urlpatterns = [
    url(r'^upload/$', views.upload,name='upload'),
    url(r'^about/$', views.about,name='about'),

]
