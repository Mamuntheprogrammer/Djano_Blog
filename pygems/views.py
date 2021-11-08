from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .models import Post,Comment
from taggit.models import Tag

from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail

from django.db.models import Count
# Create your views here.

def  post_list(request,tag_slug=None):
	object_list = Post.objects.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag,slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list,3)

	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,"pygems/list.html",{'page':page,'posts':posts,'tag':tag})


def post_details(request,year,month,day,post):
	post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
	comments = post.comments.filter(active=True)
	post_tags_ids = post.tags.values_list('id',flat=True)
	print(list(post_tags_ids))
	similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
	print(similar_posts)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
	print(similar_posts)
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
		
	else:
		comment_form = CommentForm()
	return render(request,"pygems/details.html",{'post':post,'comments':comments,
		'new_comment':new_comment,'comment_form':comment_form,'similar_posts':similar_posts})


def post_share(request,post_id):
	post = get_object_or_404(Post, id = post_id, status="published")
	sent = False
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f"{cd['name']} recomended to read { post.title }"
			message = f"Read {post.title} at {post_url}\n\n {cd['name']} \'s comments : {cd['comments']}"
			send_mail(subject,message,'ruba.bd2019@gmail.com',[cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request,"pygems/share.html",{'post':post,'form':form,'sent':sent })
	



