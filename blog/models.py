from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import ast


# class User(AbstractUser):
#     phone_number = models.CharField(unique=True, error_messages={'unique':"Uniqqq"}, max_length=13)
#     firstname = models.CharField(max_length=30, blank=True)
#     lastname = models.CharField(max_length=30, blank=True)



class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Category(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, default='')
    parent = models.ForeignKey(Category, related_name='sub', default=None)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50, default='')
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    cat = models.ForeignKey(Subcategory, related_name='Companycategory', default=None)
    def __str__(self):
        return self.name


class Post(models.Model):
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, default='', blank=True, null=True)
    q = models.IntegerField(default='', blank=True, null=True)
    title = models.CharField(max_length=200)
    text = RichTextField()
    post_image = models.ImageField(upload_to="postimage/", blank=True, null=True)
    post_image2 = models.ImageField(upload_to="postimage/", blank=True, null=True)
    post_image3 = models.ImageField(upload_to="postimage/", blank=True, null=True)
    short_text = models.TextField(max_length=120, default="")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    past_price = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=False, null=False, default=0)
    # category = models.ManyToManyField(Category, through='Category', related_name='Postcategory')
    categories = models.ForeignKey(Subcategory, related_name='Postcategory', default=None)

    def true_likes(self):
        return self.favourites_set.filter(active = True).count()

    def __unicode__(self):
        return self.title

    # @property
    # def likes(self):
    #     return Like.objects.filter(post=self)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Favourites(models.Model):
    user = models.ForeignKey(User)
    postt = models.ForeignKey(Post)
    active = models.BooleanField(default=False)



class Comment(models.Model):
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name="comments")
    text = models.TextField()
    ts = models.DateTimeField(default=timezone.now)
