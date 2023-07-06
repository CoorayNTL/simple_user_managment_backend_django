from django.contrib import admin
from django.urls import path
from . import views
# from .views import email_settings, push_settings
# import notifications.urls

urlpatterns = [
   path ("",views.home,name='home'),
   path("signup",views.signup,name='signup'),
   path("activate/<uidb64>/<token>",views.activate,name="activate"), #this is the url for the activation link
   path("signin",views.signin,name='signin'),
   path("signout",views.signout,name='signout'),
   # path('email-settings/', email_settings, name='email_settings'),
   # path('push-settings/', push_settings, name='push_settings'),
   # path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
 
]
