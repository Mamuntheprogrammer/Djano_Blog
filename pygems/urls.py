from django.urls import path
from . import views

app_name = 'pygems'

urlpatterns = [
#post view
path('',views.post_list,name='post_list')
]