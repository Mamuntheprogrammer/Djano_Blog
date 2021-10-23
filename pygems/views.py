from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .models import Post
# Create your views here.

def  post_list(request):
	object_list = Post.objects.all()
	paginator = Paginator(object_list,3)
	page = int(request.GET.get('page',1))
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(page)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request,"pygems/list.html",{'posts':posts})

def post_details(request,year,month,day,post):
	post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
	return render(request,"pygems/details.html",{'post':post})

