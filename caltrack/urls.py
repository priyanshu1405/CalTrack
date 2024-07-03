from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('mealadd.html', views.mealadd),
    path('profile.html', views.profile),
    path('editprofile.html', views.editprofile),
    path('healthnotes.html', views.healthnotes),
    path('customrecipes.html', views.customrecipes),
    path('login.html', views.login),
    path('signup.html', views.signup),
    path('home.html', views.home)
]

 