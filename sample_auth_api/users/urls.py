from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', include('trench.urls')),
    path('auth/signup', views.UserSignupApiView.as_view(), name='signup'),
    path('auth/token', views.CreateTokenView.as_view(), name='token'),
    path('auth/self', views.AuthenticatedUserView.as_view(), name='self'),
]
