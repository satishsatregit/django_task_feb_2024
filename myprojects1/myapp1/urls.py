# urls.py
from django.urls import path
from .views import UserRegistration, UserLogin
from . import views
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path("seed_database/",views.create_admin,name="seed_database")
    path("content_detail/",views.Admin_content_detail,name="content_detail")
]
