from django.urls import path
from .views import login_view, home_view
from .views import evaluation_list
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('evaluations/', evaluation_list, name='evaluation_list'), 
    path('register/', views.register_view, name='register'),
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
]
