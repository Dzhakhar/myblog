from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import blog.urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
    # (r'^ckeditor/', include('ckeditor_uploader.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)