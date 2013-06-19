from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('members.views',
	url(r'^(?P<key>\w+)/delete','delete'),
	url(r'^create','edit'),
	url(r'^(?P<key>\w+)','edit'),
	url(r'^','list'),
)