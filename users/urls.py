from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_registration),
    path('me/', me),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
]
