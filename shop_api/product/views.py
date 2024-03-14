from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .models import Product,Category,Review

@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductSerializer(products,many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_detail_api_view(request,id):
    try:
        product = Product.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product,many=False).data
    return Response(data=data)

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories,many=True).data
    return Response(data=data)

@api_view(['GET'])
def category_detail_api_view(request,id):
    try:
        category = Category.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category,many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews,many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review,many=False).data
    return Response(data=data)