from django.urls import path
from . import views
urlpatterns = [
    path('registration/',views.RegisterView.as_view()),
    path('authentication/',views.LoginView.as_view()),
    path('confirm/',views.CodeView.as_view())
]