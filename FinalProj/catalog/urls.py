from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'), 
    path('register/', views.register, name='register'),
   # path('display-items/', views.catalog, name='display_items'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('rate_item/<int:item_id>/', views.rate_item, name='rate_item'),
    path('get_ratings/<int:item_id>/', views.get_ratings, name='get_ratings'),
]   