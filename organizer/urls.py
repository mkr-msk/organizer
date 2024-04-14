from django.urls import path
from events import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('events/new', views.new_list, name='new_list'),
    path('events/<str:list_id>/', views.view_list, name='view_list'),
    path('events/<str:list_id>/add_item', views.add_item, name='add_item'),
]
