from django.urls import path, include, re_path

from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/v1/register/', RegisterAPIView.as_view(), name='register'),

    path('api/v1/login/', LoginAPIView.as_view(), name='login'),

    path('api/v1/logout/', LogoutAPIView.as_view(), name='logout'),

    path('api/v1/restoran/',RestaurantAPIView.as_view(),name='restaurant'),
    path('api/v1/restoran/<int:pk>/', RestaurantAPIView.as_view(), name='restaurant'),

    path('api/v1/restoran/<int:pk>/menu/', MenuApiView.as_view(), name='menu'),
    path('api/v1/restoran/<int:pk>/menu/<str:deta>', MenuApiView.as_view(), name='menu'),

    path('api/v1/vote/<int:menu_id>', VoteAPIView.as_view(), name='vote'),

    path('api/v1/results/',ResultsAPIView.as_view(),name="results"),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new

]
