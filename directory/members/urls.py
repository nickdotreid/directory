from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('members.views',
	url(r'^login','create_or_login'),
	url(r'^(?P<key>\w+)/delete','delete'),
	url(r'^(?P<key>\w+)','edit'),
	url(r'^','list'),
)