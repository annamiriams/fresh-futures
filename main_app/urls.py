from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('test-maps/', views.test_maps, name='test_maps'),
]
