from django.http import Http404
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, RedirectView
from braces.views import SelectRelatedMixin
from django.contrib import messages
from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

from . import models


@login_required
def CreatePost(request):
    primary = Group.objects.get(pk__iexact=request.POST.get('group'))
    if request.method == 'POST':
        try:
            post = models.Post()
            post.message = request.POST.get('message')
            post.group = Group.objects.get(pk__iexact=request.POST.get('group'))
            post.user = request.user
            post.save()
        except:
            messages.warning(request,'Message is corrupted!')
    else:
        messages.info(request,'error: The post was not successfully created. Please enter a message')
    return redirect('groups:group_details', pk=primary.pk)


#
# class DeletePost(SelectRelatedMixin, DeleteView):
#     model = models.Post
#     select_related = ("user", "group")
#     success_url = reverse_lazy("groups:group_list")
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user_id=self.request.user.id)
#
#     def delete(self, *args, **kwargs):
#         messages.success(self.request, "Post Deleted")
#         return super().delete(*args, **kwargs)
#
@login_required
def DeletePost(request, id):
    context = {}
    primary = Group.objects.get(pk__iexact=request.POST.get('group'))
    model = models.Post
    obj = get_object_or_404(model, id=request.POST.get('post_name'))
    print(obj)
    if request.method == "POST":
        obj.delete()

    return redirect('groups:group_details', pk=primary.pk)