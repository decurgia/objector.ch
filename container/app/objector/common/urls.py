from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name="home"),
    path("dashboard/", views.DashboardTemplateView.as_view(), name="dashboard"),
    path("logout/", views.LogoutRedirectView.as_view(), name="logout"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("user/<int:pk>/change/", views.UserUpdateView.as_view(), name="user-update"),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]
