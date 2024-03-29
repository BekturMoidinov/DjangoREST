from . import views
from django.urls import path
urlpatterns = [
    path('', views.product_list_api_view),
    path('<int:id>/', views.product_detail_api_view),
    path('categories/', views.category_list_api_view),
    path('categories/<int:id>/', views.category_detail_api_view),
    path('reviews/', views.review_list_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view)
]