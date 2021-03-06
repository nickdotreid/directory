from django.shortcuts import render, get_object_or_404
from annoying.functions import get_object_or_None
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
import json

from django import forms

from django.views.decorators.csrf import csrf_protect

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from members.models import Member

from django.contrib import messages

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

from django.contrib.auth import authenticate, login

def edit(request, key=None):
	member = get_object_or_404(Member, key=key)
	if 'token' in request.REQUEST:
			token = request.REQUEST['token']
			token_gen = PasswordResetTokenGenerator()
			if token_gen.check_token(member,token):
				member.backend = 'django.contrib.auth.backends.ModelBackend' # from: http://stackoverflow.com/questions/2787650/manually-logging-in-a-user-without-password
				login(request, member)
				return HttpResponseRedirect(reverse(edit,kwargs={
					'key':member.key,
					}))	
	if request.method == 'POST':
		form = MemberForm(request.POST, instance=member)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(edit,kwargs={
				'key':member.key,
				}))
	form = MemberForm(instance=member)
	return render(request, 'members/form.html', {
		'member': member,
		'form':form
		})

class MemberForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(forms.ModelForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.add_input(Submit('submit', 'Save'))
	class Meta:
		model = Member
		fields = ['name', 'title', 'website']

def delete(request, key=None):
	member = get_object_or_404(Member, key=key)
	member_name = member.name
	member.delete()
	messages.success(request, '%s has been deleted.' % (member_name))
	return HttpResponseRedirect(reverse(list))

def list(request, visible=5):
	if 'member' in request.REQUEST:
		key = request.REQUEST['member']
		members = []
		members.append(Member.objects.get(key=key))
		for member in Member.objects.exclude(key=key).order_by('?').all():
			members.append(member)
	else:
		members = Member.objects.order_by('?').all()
	if 'all' not in request.REQUEST:
		members = members[:visible]
	if request.is_ajax():
		return HttpResponse(
			json.dumps({
				'members': members,
			}),
			'application/json'
			)
	return render(request, 'members/list.html',{
			'members': members,
			'form':EmailForm(),
		})

def create_or_login(request):
	if not request.method == 'POST':
		return HttpResponseRedirect(reverse(list))
	form = EmailForm(request.POST)
	if not form.is_valid():
		return render(request, 'members/login.html',{
			'form':form,
		})
	data = form.cleaned_data
	member = get_object_or_None(Member, email=data['email'])
	if not member:
		member = Member(email=data['email'])
		member.save()
	member_url = reverse(edit,kwargs={
		'key':member.key,
		})
	token_gen = PasswordResetTokenGenerator()
	token = token_gen.make_token(member)
	try:
		send_mail(
			'Your Nick Reid Directory Profile',
			'Follow this link to update your profile: %s?token=%s' % (member_url, token),
			'admin@nickreid.com',
			[member.email],
			fail_silently=False,
			)
	except:
		messages.error(request, 'There was an error sending email to %s', member.email)
	messages.success(request, 'An email has been sent to %s.' % (member.email))
	return HttpResponseRedirect(reverse(list))

class EmailForm(forms.Form):
	def __init__(self, *args, **kwargs):
			super(forms.Form, self).__init__(*args, **kwargs)
			self.helper = FormHelper()
			self.helper.form_action = reverse(create_or_login)
			self.helper.add_input(Submit('submit', 'Send'))
	email = forms.EmailField(label='Email address', required=True)