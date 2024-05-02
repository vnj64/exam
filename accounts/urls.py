from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from .views import RegistrationView, ProfileView, AddBalance

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    path('add-balance/', AddBalance.as_view(), name='add-balance'),
]
