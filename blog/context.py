from .models import Post, Category, Subcategory, Favourites
from .models import User
from cart import Cart

def categories(request):
    category = Category.objects.all()
    return {'user': request.user, 'category': category}


def cart_count(request):
    if not request.user.is_anonymous():
        a = request.user.post_set.all().count()
        return {'cart_count': a}

    else:
        c = Cart(request)
        return {'cart_count': c.count()}
