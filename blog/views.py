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
from .models import Post, Category, Subcategory, Favourites
import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator



def loadmore(request):
    for i in request.POST['p']:
        try:
            pagenum = int(request.POST['p'])
            posts = Post.objects.all()
            paginator = Paginator(posts, 9)
            page = paginator.page(pagenum)
        except:
            page = []

    return render(request, 'blog/pages.html', {'posts':page})



def profile(request):
    if not request.user.is_anonymous():
        favs = request.user.favourites_set.filter(active = True)
        return render(request, 'blog/profile.html', {'favs': favs})

    else:
        return redirect('/accounts/login/')



def like(request):
    post = Post.objects.filter(id = int(request.POST['i']))
    f = Favourites.objects.filter(user=request.user, postt=post[0])
    if f.count() == 0:
        Favourites(user=request.user, postt=post[0], active = True).save()
    else:
        f = Favourites.objects.filter(user=request.user, postt=post[0]).first()
        f.active = not f.active
        f.save()

    gf = post[0].favourites_set.filter(active=True).count()

    print f.active
    return render(request, 'blog/likes.html', {'like':gf})



def base(request):
    if request.user.is_authenticated():
        # cart_count = request.user.post_set.all().count()
        posts = Post.objects.all()
        # for p in posts:
        #     p.favourites_set.filter(active=True)
        category = Category.objects.all()
        paginator = Paginator(posts, 9)
        page = paginator.page(1)
        for i in paginator.page(2):
            print i

        return render(request, 'blog/base.html', {
            'posts': page,
            'user': request.user,
            'category': category})

    else:
        posts = Post.objects.all()
        paginator = Paginator(posts, 9)
        page = paginator.page(1)
        category = Category.objects.all()
        return render(request, 'blog/base.html', {'posts': page, 'category': category})





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
        return render(request, 'blog/post_edit.html', {'form': form})
        form = PostForm()


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

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'blog/login.html', c)


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
    return redirect('/')


def invalid_login(request):
    return render(request, 'blog/invalid_login.html')


def logout(request):
    auth.logout(request)
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


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
    return render(request, 'blog/register.html', args)


def register_success(request):
    return render(request, 'blog/register_success.html')


def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    search_posts = Post.objects.filter(title__contains=search_text)

    return render(request, 'blog/ajax_search.html', {'search_posts': search_posts})


def sub_filter(request, pk):
    sub = Subcategory.objects.filter(name=pk)
    sub_name = pk
    return render(request, 'blog/sub_filter.html', {'sub': sub, 'sub_name': sub_name})


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

    return redirect('blog.views.get_cart')


def remove_from_cart(request, pk):
    product = Post.objects.get(id=pk)
    cart = Cart(request)
    removed_product = product

    cart.remove(product)
    if request.user.is_authenticated():
        request.user.remove_from_product_list(product)

    return render(request, 'blog/cart.html', {'removed_product': removed_product})


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
    return render(request, 'blog/indexfile.html', {'headers':header, 'links':links})


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
