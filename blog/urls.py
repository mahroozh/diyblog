from django.urls import path, include 
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import custom_logout

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),  # /blog/
    path('blogs/', views.blog_list, name='blog_list'),  # list of posts (paginated)
    path('bloggers/', views.blogger_list, name='blogger_list'),
    path('register/', views.register, name='register'),
    path('create/', views.create_post, name='create_post'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('blogger/<int:pk>/', views.blogger_detail, name='blogger_detail'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('<int:pk>/create/', views.create_comment, name='create_comment'),
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

]


auth_views.PasswordResetView.as_view(
    template_name='users/password_reset.html',
    subject_template_name='registration/password_reset_subject.txt',
    email_template_name='registration/password_reset_email.html',
    html_email_template_name='registration/password_reset_email.html',

)

