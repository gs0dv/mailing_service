from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path


from users.apps import UsersConfig
from users.views import RegisterView, recovery_password, verification, UserUpdateView, UserListView, \
    toggle_activity_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('recovery/', recovery_password, name='recovery'),
    path('verify/<verification_key>', verification, name='verify'),
    path('users/list/', UserListView.as_view(), name='users_list'),
    path('users/toggle_activity_user/<int:pk>', toggle_activity_user, name='toggle_activity_user'),
]
