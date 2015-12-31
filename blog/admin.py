from django.contrib import admin
from ckeditor.fields import RichTextField
from .models import Post
from .models import Category
from .models import Subcategory

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Subcategory)
# Register your models here.

