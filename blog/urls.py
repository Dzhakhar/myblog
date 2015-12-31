from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/auth/$', views.auth_view),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/invalid/$', views.invalid_login),
    url(r'^accounts/register/$', views.register_user),
    url(r'^accounts/register_success/$', views.register_success),
    url(r'^post/like/(?P<pk>[0-9]+)/$', views.post_like, name='post_like'),
    url(r'^search/$', views.search_titles),
    url(r'^post/sub/(?P<pk>[0-9 A-Z a-z]+)', views.sub_filter),
    url(r'^add_to_cart/(?P<pk>[0-9]+)/(?P<q>[0-9]+)', views.add_to_cart),
    url(r'^remove_from_cart/(?P<pk>[0-9]+)', views.remove_from_cart),
    url(r'^get_cart/', views.get_cart),
]
