from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('test-maps/', views.test_maps, name='test_maps'),
    # path('user/', views.UserUpdate.as_view(), name='user-update'),
    path('start/', views.start, name='start'),
    path('start/survey/', views.GardenCreate.as_view(), name='garden-create'),
    path('profile/', views.profile, name='profile'),
]
