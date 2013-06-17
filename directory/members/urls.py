from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('members.views',
	url(r'^','list'),
)