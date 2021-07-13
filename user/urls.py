from django.contrib.auth import views as auth_views
from django.urls import path
from user.views import UserSignUpView, UserLoginView, UserPurchaseListView

app_name = 'user'

urlpatterns = [
    path('register/', UserSignUpView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('purchases/', UserPurchaseListView.as_view(), name='purchases'),
]
