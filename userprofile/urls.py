from userprofile import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('register/',views.register,name='register'),
    path('AboutUs/',views.AboutUs,name='AboutUs'),
    path('logout',views.logoutUser,name = 'logout'),
    path('ContactUs/',views.ContactUs,name='ContactUs'),
    path('services/', views.services, name='services'),
    path('terms/', views.terms, name='terms'),
    path('analytics/', views.analytics, name='analytics'),
]
