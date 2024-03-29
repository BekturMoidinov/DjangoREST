from django.urls import path
from . import views
urlpatterns = [
    path('registration/',views.register_api_view),
    path('authentication/',views.authentication_api_view),
    path('confirm/',views.confirm_api_view)
]