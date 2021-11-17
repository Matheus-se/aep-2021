from django.urls import path
from . import views
from .views import FarmerListView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'farmer'

urlpatterns = [
    path('register', views.register_farmer_view, name="farmer-post"),
    path('<id>/', views.list_farmers_view, name="farmer-get"),
    path('login', obtain_auth_token, name="login"),
    path('list', FarmerListView.as_view(), name="farmer-list"),
    path('account', views.farmer_account_view, name="farmer-account"),
    path('update', views.update_farmer_view, name="farmer-update"),
    path('delete', views.delete_farmer_view, name="farmer-delete"),
]
