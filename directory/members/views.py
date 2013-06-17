from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.views.decorators.csrf import csrf_protect

from members.models import Member

from django.contrib import messages

from random import shuffle

def detail(request, key):
	member = get_object_or_404(Member, key=key)
	return render(request, 'members/detail.html', {
		'member':member,
	})

def list(request):
	members = Member.objects.all()
	shuffle(members)
	return render(request, 'members/list.html',{
			'members': members,
		})