from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, PlantDiseaseDetectionAPIView, UserUpdateView,StatsView,UserDetectionListAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('predict/', PlantDiseaseDetectionAPIView.as_view(), name='plant-disease-prediction'),
    path('api/user/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/stats/', StatsView.as_view(), name='api-stats'),
    path('user/detections/', UserDetectionListAPIView.as_view(), name='user-detections'),



]
