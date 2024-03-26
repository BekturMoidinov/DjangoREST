from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer,ProductValidationSerializer,CategoryValidationSerializer,ReviewValidationSerializer
from .models import Product,Category,Review

@api_view(['GET','POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.prefetch_related('reviews').all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get('title')
        price = serializer.validated_data.get('price')
        description = serializer.validated_data.get('description')
        category_id= serializer.validated_data.get('category_id')
        Product.objects.create(title=title, price=price, description=description, category_id=category_id)

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def product_detail_api_view(request,id):
    try:
        product = Product.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.price = serializer.validated_data.get('price')
        product.description = serializer.validated_data.get('description')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = CategoryValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        Category.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def category_detail_api_view(request,id):
    try:
        category = Category.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = CategoryValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ReviewValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get('text')
        star=serializer.validated_data.get('star')
        product_id=serializer.validated_data.get('product_id')
        Review.objects.create(product_id=product_id,star=star,text=text)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def review_detail_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.star = serializer.validated_data.get('star')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)