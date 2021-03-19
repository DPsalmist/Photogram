from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Photo, Comment
from .forms import PhotoForm, CommentForm
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views.generic import ( 
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
#added something
# class PhotoListView(ListView):
# 	model = Photo
# 	template_name = 'photos/gallery.html' #<app>/<model>/<viewtypet>.html
# 	context_object_name = 'my_photos'
# 	ordering = ['-created'] #to make the newest post show at the top
# 	paginate_by = 3

class UserPhotoListView(ListView):
	model = Photo
	template_name = 'photos/user_photos.html' 
	context_object_name = 'my_pics'
	ordering = ['-created'] 
	paginate_by = 3

	def get_queryset(self):
		#getting the username from the url 
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Photo.objects.filter(owner=user).order_by('-created')

class PhotoDetailView(DetailView):
	model = Photo

class PhotoCreateView(LoginRequiredMixin, CreateView):
	model = Photo
	fields = ['category', 'image', 'description', 'tags']

	#overriding the form valid method
	def form_valid(self, form):
		form.instance.owner  = self.request.user
		return super().form_valid(form)

class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Photo
	fields = ['category', 'description']
	
	def form_valid(self, form):
		form.instance.owner  = self.request.user
		return super().form_valid(form)

	#test function to make only an authorised user update a photo
	def test_func(self):
		photo = self.get_object()
		if self.request.user == photo.owner:
			return True
		return False

class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Photo
	success_url = '/'

	#test function to make only an authorised user delete a post
	def test_func(self):
		photo = self.get_object()
		if self.request.user == photo.owner:
			return True
		return False

# Create your views here.
def gallery(request):
	category = request.GET.get('category')
	object_list = Photo.objects.all()
	if category == None:
		photos = Photo.objects.all()
	else:
		object_list = Photo.objects.filter(category__name = category)

	paginator = Paginator(object_list, 6)
	page = request.GET.get('page')
	try:
		photos = paginator.page(page)
	except PageNotAnInteger:
		photos = paginator.page(1) #If page is not an integer deliver the first page
	except EmptyPage:
		photos = paginator.page(paginator.num_pages)

	categories = Category.objects.all()
	context = {
		'categories':categories,
		'photos':photos, 
		'category':category, 
		'page':page,
	}
	return render(request, 'photos/gallery.html', context)

#function detailview
def viewPhoto(request, pk):
	photo = get_object_or_404(Photo, id=pk)
	user = request.user
	#photo_det = Photo.objects.filter(owner=user).order_by('-created')

	# List of active comments for this post
	comments = photo.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		# A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to db yet
			new_comment = comment_form.save(commit=False)
			# Assign the current photo to the comment
			new_comment.photo = photo
			new_comment.save()
	else:
		comment_form = CommentForm()

	context = {
		'comments': comments, 
		'new_comment': new_comment, 
		'comment_form': comment_form,
		'photo':photo,
		'user':user,
		#'photo_det':photo_det,
    }
	return render(request, 'photos/photo.html', context)

#function userphotolistview
def userPhotoList(request, username):
	current_user = request.user
	photo_owner = Photo.objects.filter(owner=current_user.id)

	username = get_object_or_404(User, username='username')
	photo_list = Photo.objects.filter(owner=username).order_by('-created')

	context = {
		'user':current_user,
		'photo_owner':photo_owner,
		'username':username,
		'photo_list':photo_list,
	}
	return render(request, 'photos/user_photos.html', context)

def aboutPage(request):
	return render(request,'photos/about.html')

@login_required
def addPhoto(request):
	photo = Photo.objects.all()
	user = request.user	
	current_user = Photo.objects.filter(owner=user.id)
	categories = Category.objects.all()
		
	if request.method == 'POST':
		# Form has been sent
		form = request.POST
		image = request.FILES.get('mypic')
		user = request.user
		#user = get_object_or_404(User)
		current_user_photo = Photo.objects.filter(owner=user.id)
		# owner = form.owner.id
		# print('owner:',owner)
		
		# Are both category fields filled
		if form['category'] != 'none':
			category = Category.objects.get(id=form['category'])
		elif form['category_new'] != '':
			category, created = Category.objects.get_or_create(name=form['category_new'])
		else:
			category = None
		photo = Photo.objects.create( category = category,
								description = form['description'],
								image = image, owner=current_user_photo.id)

		messages.success(request, f'Photo added successfully!')	
		return redirect('/')
	#context = {'categories':categories, 'form':form,'user':user,'photo':photo}
	context = {'categories':categories, 'user':user}
	return render(request, 'photos/add.html', context)

# user likes view
@login_required
@require_POST
def image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id=image_id)
			if action == 'like':
				image.users_like.add(request.user)
			else:
				image.users_like.remove(request.user)
			return JsonResponse({'status':'ok'})
		except:
			pass
	return JsonResponse({'status':'error'})

class SearchResultsView(ListView):
	model = Photo
	template_name = 'photos/search_result.html'

	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = Photo.objects.filter(
			Q(description__icontains=query) | Q(category__icontains=query))
		return object_list

