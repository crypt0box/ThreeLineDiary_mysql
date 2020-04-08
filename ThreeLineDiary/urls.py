from django.urls import path
from . import views

app_name = 'ThreeLineDiary'

urlpatterns = [
    path('home', views.IndexView.as_view(), name='home'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create_complete/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('post_create/<int:user_pk>/', views.PostCreate.as_view(), name='post_create'),
    path('icon_update/<int:pk>/', views.IconUpdate.as_view(), name='icon_update'),
    path('about/', views.About.as_view(), name='about'),
]
