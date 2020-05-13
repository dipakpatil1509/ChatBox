from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView,ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from groups.models import Group, GroupMember


User = get_user_model()

#
# class UsersListView(LoginRequiredMixin,ListView):
#     login_url = 'accounts:login'
#     context_object_name = 'users_names'
#     model = User
#     template_name = 'contacts/users_list.html'
#     def get_context_data(self, **kwargs):
#         context = super(UsersListView, self).get_context_data()
#         context['group_details'] = Group.objects.all()
#         return context
@login_required
def UserListView(request):
    user1 = User.objects.all()
    try:
        if request.method == 'POST':
            group = get_object_or_404(Group, pk__iexact=request.POST.get('groups_pk'))

            try:
                if request.user.username == group.owner:
                    UserPrimarykey = get_object_or_404(user1, pk=request.user.pk)
                    GroupMember.objects.create(user=UserPrimarykey, groups=group)

            except:
                pass
            return render(request,'contacts/users_list.html',{'users_names':user1,'group_details':group, 'show':'True'})
    except:
        return render(request, 'contacts/users_list.html', {'users_names': user1,'show':'False'})
    else:
        return render(request,'contacts/users_list.html',{'users_names':user1, 'show':'False'})




@login_required
def SearchListPost(request):
    user = User.objects.all()
    if request.method == 'POST':
        text = request.POST['search']
        try:
            user = User.objects.filter(username__iexact=text)
        except:
            try:
                user = User.objects.filter(first_name__iexact=text)
            except:
                try:
                    user = User.objects.filter(last_name__iexact=text)
                except:
                    try:
                        user = User.objects.filter(email__iexact=text)
                    except User.DoesNotExist:
                        messages.info(request, 'Does Not Match!!')
                        return redirect('contacts:user_list')
        if len(user) == 0:
            messages.info(request, 'Does Not Match!!')
            return redirect('contacts:user_list')
        try:
            group = Group.objects.get(pk__iexact=request.POST['groups_name'])
            return render(request, 'contacts/search_list.html',
                          {'search_lists': user, 'group_details': group, 'show': 'True'})
        except:
            pass

    return render(request,'contacts/search_list.html',{'search_lists':user,'show':'False'})



