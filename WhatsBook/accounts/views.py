from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy,reverse
from . import models
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class Home(TemplateView):
    template_name = 'home.html'

class Signup(CreateView):
    form_class = forms.Userform
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'



class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class Profile(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile_details.html'

class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:login'
    fields = ('first_name','last_name','email')
    model = User
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')

class UserProfile(LoginRequiredMixin, DetailView):
    login_url = 'accounts:login'
    context_object_name = 'user_details'
    template_name = 'accounts/user_profile.html'
    model = User
    def get_queryset(self, **kwargs):
        return User.objects.filter(pk__iexact=self.kwargs.get('pk'))
