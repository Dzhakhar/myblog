from .models import Post, Like, Category, Subcategory

def categories(request):
    category = Category.objects.all()
    return {'user': request.user, 'category': category}