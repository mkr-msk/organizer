from django.urls import path
from events import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('events/new', views.new_list, name='new_list'),
    path('events/list1/', views.view_list, name='view_list'),
]
