from django.shortcuts import render,get_object_or_404

from .models import Post
# Create your views here.

def  post_list(request):
	posts = Post.objects.all()
	return render(request,"pygems/base.html",{'posts':posts})

