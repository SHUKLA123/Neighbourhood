"""allauth1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from testapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
#For Registration and signup
from django.contrib.auth import views as auth_views
from users import views
from bussiness import views as as_views
from comment import views as as_views1
#comment
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^friendship/', include('friendship.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'home/',views.home,name = 'home'),
    url(r'tweet/',views.tweet_view,name = 'tweet'),
    url(r'^accounts/', include('allauth.urls')),
#This of registration and login and logout
    url(r'^$',views.register,name = 'register'),
    url(r'login/',auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    url(r'logout/',auth_views.LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    url(r'password-reset/',auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'),name = 'password_reset'),
    url(r'^password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name =  'password_reset_done.html'), name='password_reset_done'),
    url(r'^password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name =  'password_reset_confirm.html'), name='password_reset_confirm'),
#search bar
    url(r'^search/$',views.search,name = 'search'),
    url(r'^user/follow/$', views.user_follow, name='user_follow'),
#Add User_Profile
    url(r'^user/(?P<username>.\w+)/$', views.ProfileView),
    url(r'^people', views.follow_people, name = 'people'),
    url(r'^post/', views.post_list,name = 'post'),
    url(r'^like/$', views.image_like, name = 'like'),
#group chat
    url('chat/', include('chat.urls')),
#bussiness
    url(r'^buss_name/', as_views.bussiness_form, name = 'buss_make'),
    url(r'^buss/', as_views.display, name = 'buss'),
    url(r'^nearby/', as_views.nearby, name = 'nearby'),
    url(r'^user/(?P<user_id>\d+)/$', as_views.request_user),
# comments model

    # url(r'^news/(?P<pincode>\d+)/$',as_views1.news),
    url(r'^news/(?P<pincode>\d+)/$',as_views1.news),
    url(r'^problem/$',as_views1.write_problem,name = 'problem'),
    url(r'^preply/$',as_views1.write_reply,name = 'problem-reply'),


#comment tweet
    url(r'^comment/$',views.write_comment,name='comment'),
    url(r'^reply/$',views.write_reply,name='reply'),

#map
    url(r'^map/',views.map),

#address update
    url(r'^address_update/',views.AddressUpdateView,name = 'address_update'),

#Event
    url(r'^event-like/',views.event_like,name = 'eventlike'),
    url(r'^event/',views.event_create,name = 'event'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
