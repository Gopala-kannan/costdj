from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('profile', views.profile_api),
    path('profile/<int:id>', views.profile_api),
    path('spendamount', views.spendamount_api),
    path('spendamount/<int:id>', views.spendamount_api),
    path('details/', views.details, name='details'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile_create/', views.profile_create, name='profile_create'),
    path('spendamount_create', views.spendamount_create, name='spendamount_create'),
]