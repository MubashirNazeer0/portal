from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),

    path('register/', user_views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True),name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/welcome.html'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome'), name='logout'),
    
    path('profile/', user_views.profile, name='profile'),
    path('view_user/<int:id>', user_views.view_profile, name='user_profile'),
    path('update_password', user_views.update_password, name='update_password'),
    # path('advertisementsforwelcome/', views.advertisement_listforwelcome, name='advertisement_listforwelcome'),  

]
