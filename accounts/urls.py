from django.urls import path

from accounts import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'accounts'
urlpatterns = [
    # JWT token endpoints
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User registration and login endpoints
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('login/', views.LoginUser.as_view(), name='login_user')
]