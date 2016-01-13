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
        category = Category.objects.all()
        return render(request, 'blog/base.html', {'posts': posts, 'category': category})


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
    product.q = q
    cart = Cart(request)
    added_product = product
    product_user = 0;
    if request.user.is_authenticated():
        product.q = q
        request.user.post_set.add(product)
        product_user = request.user.post_set
        request.products = request.user.post_set.filter(user=request.user)
    else:
        cart.add(product, product.price, q)

    return render(request, 'blog/cart.html', {'added_product': added_product, 'cart':Cart(request), 'products': product_user})


def remove_from_cart(request, pk):
    product = Post.objects.get(id=pk)
    cart = Cart(request)
    removed_product = product

    cart.remove(product)
    if request.user.is_authenticated():
        request.user.remove_from_product_list(product)

    return render_to_response('blog/cart.html', {'removed_product': removed_product})


def get_cart(request):
    products = 0;
    if request.user.is_authenticated:
        if not request.user.is_anonymous():
            request.products = request.user.post_set.filter(user=request.user)

    return render(request, 'blog/cart.html', dict(cart=Cart(request)))


def lenta(request):
    url = 'http://tengrinews.kz'

    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    items = soup.findAll('div', {'class': 'ten'})
    # print items[0]
    header = []
    links = []
    for i in items[0]:
        span = i.find('span')
        a = i.find('a')
        if type(a) == int:
            print ''
        else:
            href = a.get('href')
            full_href = url + href
            links.append(full_href)

        if type(span) == int:
            print ''
        else:
            header.append(span.text);
            print span.text

    header = header[1:7]
    return render_to_response('blog/indexfile.html', {'headers':header, 'links':links})


def lenta_item(request):
    url = 'http://tengrinews.kz'

    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    items = soup.findAll('div', {'class': 'ten'})
    # print items[0]
    for i in items[0]:
        span = i.find('span')
        a = i.find('a')
        if type(a) == int:
            print ''
        else:
            href = a.get('href')
            full_href = url + href
            print full_href
            r_content = requests.get(full_href)
            print(r_content.status_code)
            soup_content = BeautifulSoup(r_content.content)
            items_content = soup_content.findAll('div', {'class': 'text sharedText'})
            for con in items_content:
                p_content = con.findAll('p')
                frame = con.find('iframe')
                for p in p_content:
                    try:
                        print p.text
                        print url + p.img.get('src')
                        print frame.get('src')
                    except:
                        pass
