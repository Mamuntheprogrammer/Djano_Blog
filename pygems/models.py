from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import	TaggableManager
from tinymce import models as tmodels

# Create your models here.

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status="Published")


class Post(models.Model):
	""" Post Model"""
	# custom manager
	objects = models.Manager()
	published = PublishedManager()


	STATUS_CHOICES = (('draft','Draft'),('published','Published'))
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,unique_for_date='publish')
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
	body = tmodels.HTMLField(max_length=2000)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

	tags = TaggableManager()

	def get_absolute_url(self):
		return reverse('pygems:post_details',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

	class Meta:
		ordering = ('-publish',)
		
	def __str__(self):
		return self.title 


class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = tmodels.HTMLField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)
	def __str__(self):
		return f'comment by {self.name} on {self.post}'