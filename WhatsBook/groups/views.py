from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import DetailView, ListView,CreateView,DeleteView,UpdateView, RedirectView,TemplateView
from .models import Group,GroupMember
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


User = get_user_model()

class GroupListView(LoginRequiredMixin,ListView):
    login_url = 'accounts:login'
    context_object_name = 'group_lists'
    model = Group
    template_name = 'groups/group_list.html'

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data()
        context['group_details'] = Group.objects.all()
        return context

@login_required
def SearchListView(request):
    if request.method == 'POST':
        text = request.POST['search']
        try:
            search_lists = Group.objects.filter(name__iexact=text)
        except Group.DoesNotExist:
            messages.info(request, 'Does Not Match!!')
            return redirect('groups:group_list')

        if len(search_lists) == 0:
            messages.info(request, 'Does Not Match!!')
            return redirect('groups:group_list')

    return render(request,'groups/search_list.html',{'search_lists': search_lists})

class DeleteGroup(LoginRequiredMixin,DeleteView):

    login_url = 'accounts:login'
    template_name = 'groups/confirm_delete.html'
    model = Group
    success_url = reverse_lazy('groups:group_list')



class GroupDetailView(LoginRequiredMixin,DetailView):
    login_url = 'accounts:login'
    context_object_name = 'group_details'
    template_name = 'groups/group_list.html'

    model = Group
    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data()
        context['group_lists'] = Group.objects.all()
        return context
    def get_queryset(self):
        return Group.objects.filter(name__isnull=False).order_by('name')

class CreateGroup(LoginRequiredMixin,CreateView):
    login_url = 'accounts:login'
    template_name = 'groups/create_group.html'
    fields = ('name','dp','description')
    model = Group
    success_url = reverse_lazy('groups:group_list')

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner

        return super(CreateGroup, self).form_valid(form)


class UpdateGroup(LoginRequiredMixin,UpdateView):
    login_url = 'accounts:login'
    template_name = 'groups/create_group.html'
    fields = ('name', 'dp', 'description')
    model = Group
    def get_absolute_url(self):
        return reverse('groups:group_details',kwargs={'pk':self.kwargs.get('pk')})

@login_required
def JoinGroup(request):
    user=User.objects.all()
    group = get_object_or_404(Group, pk__iexact=request.POST.get("group_pk"))
    UserPrimarykey = get_object_or_404(user, pk__iexact=request.POST.get('users_name'))
    try:
        GroupMember.objects.create(user=UserPrimarykey,groups=group)

    except:
        messages.warning(request,("Warning, User is already a member of {}".format(group.name)))

    return render(request, 'contacts/users_list.html', {'users_names': user, 'group_details': group,  'show':'True'})

@login_required
def LeaveGroup(request):
    user = User.objects.all()
    group = get_object_or_404(Group, pk__iexact=request.POST.get("group_pk"))

    try:
        UserPrimarykey = get_object_or_404(user, pk__iexact=request.POST.get('users_name'))
        membership = GroupMember.objects.filter(user=UserPrimarykey,groups=group).get()
    except:
        try:
            membership = GroupMember.objects.filter(user=request.user, groups=group).get()

        except GroupMember.DoesNotExist:
            messages.warning(request,"You can't leave this group because you aren't in it.")
        else:
            membership.delete()
            messages.success(request,"Successfully left group.")
            return redirect('groups:group_details', pk=group.pk)
    else:
        membership.delete()
        messages.success(request,"Successfully remove user.")
        return render(request, 'contacts/users_list.html',
                      {'users_names': user, 'group_details': group, 'show': 'True'})

class Groupmem(LoginRequiredMixin, ListView):
    template_name = 'groups/group_members.html'
    login_url = 'accounts:login'
    context_object_name = 'group_members'
    model = Group

    def get_queryset(self, **kwargs):
        return Group.objects.get(pk__iexact=self.kwargs.get('pk'))