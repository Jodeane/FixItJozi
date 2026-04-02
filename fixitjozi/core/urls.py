from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('track/', views.track, name='track'),
    path('track/lookup/', views.track_lookup_api, name='track_lookup'),
    path('community/', views.community, name='community'),
    path('dashboard/', views.dashboard, name='dashboard'),
]