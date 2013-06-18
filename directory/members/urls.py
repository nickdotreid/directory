from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('members.views',
	url(r'^create','edit'),
	url(r'^(?P<key>\w+)/edit','edit'),
	url(r'^(?P<key>\w+)','detail'),
	url(r'^','list'),
)