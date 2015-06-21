from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
import settings
from django.views.generic import TemplateView
from cms.views import *
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cms.views.home_page', name='home'),
    url(r'^account/login/','cms.views.login_page', name='login'),
    url(r'^account/logout/','cms.views.logout_page', name='logout'),
    url(r'^account/profile/','cms.views.profile_page', name='profile'),
    url(r'^course/(?P<id>\d+)/','cms.views.course_page', name='course'),
    url(r'^join/','cms.views.join_page', name='join'),
    url(r'^post/','cms.views.post_page', name='post'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'login/stu/')
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG and settings.STATIC_URL:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)