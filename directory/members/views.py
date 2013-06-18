from django.shortcuts import render, get_object_or_404
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.views.decorators.csrf import csrf_protect

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from members.models import Member

from django.contrib import messages

from random import shuffle

def edit(request, key=None):
	member = get_object_or_None(Member, key=key)
	MemberForm = make_edit_form()
	if request.method == 'POST':
		form = MemberForm(request.POST, instance=member)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(edit,kwargs={
				'key':form.instance.key,
				}))
	form = MemberForm(instance=member)
	return render(request, 'members/form.html', {
		'member': member,
		'form':form
		})

from django.forms import ModelForm
def make_edit_form():
	class MemberForm(ModelForm):
		def __init__(self, *args, **kwargs):
			super(ModelForm, self).__init__(*args, **kwargs)
			self.helper = FormHelper()

			self.helper.add_input(Submit('submit', 'Save'))
		class Meta:
			model = Member
			fields = ['name', 'email', 'title', 'website']
	return MemberForm



def list(request):
	members = Member.objects.all()
	shuffle(members)
	return render(request, 'members/list.html',{
			'members': members,
		})