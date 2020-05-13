from django.conf.urls import url
from django.urls import reverse_lazy
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns =[
    path('', views.Home.as_view(), name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('thanks/', views.ThanksPage.as_view(), name='thanks'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                              html_email_template_name='registrations/password_reset_email.html',
                                              success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),

    path('reset_password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),


    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html',
                                                     success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),


    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
                                                                   success_url=reverse_lazy('accounts:password_change_done')),
         name='password_change'),

    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    path('profile/', views.Profile.as_view(), name='profile'),
    url(r'^update/(?P<pk>\d+)/$', views.UpdateProfile.as_view(), name='update'),
    path('profile/(?P<pk>\d+)', views.UserProfile.as_view(), name='user_profile'),


]