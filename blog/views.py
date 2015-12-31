from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from cart import Cart
from django.contrib.auth.forms import UserCreationForm
from forms import MyRegistrationForm
from django.utils import timezone
import sorl.thumbnail
from .forms import PostForm
from .models import Post, Like, Category, Subcategory
import requests
from bs4 import BeautifulSoup


# Create your views here.

def base(request):
    if request.user.is_authenticated():
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        category = Category.objects.all()

        return render(request, 'blog/base.html', {
            'posts': posts,
            'user': request.user,
            'category': category})

    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return render(request, 'blog/base.html', {'posts': posts, 'category': category, 'subcategory': subcategory})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.short_text = form.save(commit=False)
            # post.post_image = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated():
        if Like.objects.filter(author=request.user, post=post).count() == 0:
            Like.objects.create(post=post, author=request.user)
        else:
            Like.objects.filter(author=request.user, post=post).delete()
    else:
        return HttpResponseRedirect('/accounts/login/')
    return HttpResponseRedirect('')


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('blog/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('blog/loggedin.html',
                              {'full_name': request.user.username})


def invalid_login(request):
    return render_to_response('blog/invalid_login.html')


def logout(request):
    auth.logout(request)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render_to_response('blog/post_list.html', {'posts': posts})


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    args = {}
    args.update(csrf(request))
    args['form'] = MyRegistrationForm()
    print(args)
    return render_to_response('blog/register.html', args)


def register_success(request):
    return render_to_response('blog/register_success.html')


def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    search_posts = Post.objects.filter(title__contains=search_text)

    return render_to_response('blog/ajax_search.html', {'search_posts': search_posts})


def sub_filter(request, pk):
    sub = Subcategory.objects.filter(name=pk)
    sub_name = pk
    return render_to_response('blog/sub_filter.html', {'sub': sub, 'sub_name': sub_name})


def add_to_cart(request, pk, q):
    product = Post.objects.get(id=pk)
    cart = Cart(request)
    added_product = product
    cart.add(product, product.price, q)
    return render_to_response('blog/cart.html', {'added_product': added_product})


def remove_from_cart(request, pk):
    product = Post.objects.get(id=pk)
    cart = Cart(request)
    removed_product = product
    cart.remove(product)
    return render_to_response('blog/cart.html', {'removed_product': removed_product})


def get_cart(request):
    return render_to_response('blog/cart.html', dict(cart=Cart(request)))

