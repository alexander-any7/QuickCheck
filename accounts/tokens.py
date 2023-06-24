from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

def create_jwt_pair_for_user(user:User):
    # Create JWT pair (access token and refresh token) for the given user
    refresh = RefreshToken.for_user(user)

    # Generate the access token and refresh token as strings
    tokens = {
        "access" : str(refresh.access_token),
        "refresh" : str(refresh)
    }
    return tokens