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
    url(r'^accounts/register/','cms.views.register_page', name='register'),
    url(r'^accounts/login/','cms.views.login_page', name='login'),
    url(r'^accounts/logout/','cms.views.logout_page', name='logout'),
    url(r'^accounts/profile/','cms.views.profile_page', name='profile'),
    url(r'^course/(?P<id>\d+)/','cms.views.course_page', name='course'),
    url(r'^join/','cms.views.join_page', name='join'),
    url(r'^post/','cms.views.post_page', name='post'),
    url(r'^add_new_course/','cms.views.add_new_course_page', name='add_new_course'),
    url(r'^discuss/$','cms.views.all_discuss_page',name='all_discuss'),
    url(r'^discuss/(?P<id>\d+)/','cms.views.single_discuss_page', name='single_discuss'),
    url(r'^question/$','cms.views.all_question_page',name='all_question'),
    url(r'^question/(?P<id>\d+)/','cms.views.single_question_page', name='single_question'),
    #url(r'login/stu/')
    url(r'^admin/', include(admin.site.urls)),
)
