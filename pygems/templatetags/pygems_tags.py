from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
	print(Post.objects.count())
	return Post.objects.count()