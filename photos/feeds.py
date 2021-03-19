from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Photo
   
class LatestPhotoFeed(Feed):
  title = 'My Photos'
  link = reverse_lazy('gallery')
  description = 'Latest Pictures.'

  def items(self):
    return Photo.objects.all()[:5]

  # def item_title(self, item):
  #   return item.title

  def item_description(self, item):
    return truncatewords(item.description, 30)