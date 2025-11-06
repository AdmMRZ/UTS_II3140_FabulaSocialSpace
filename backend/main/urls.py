from django.urls import path
from . import views

urlpatterns = [
    path('auth/google', views.auth_google),
    path('auth/logout', views.logout),
    path('menu', views.menu_list),
    path('order', views.order_create),
    path('tenant', views.tenant_create),
]