from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product,Category,Review

class CategorySerializer(serializers.ModelSerializer):
    count_products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = 'name count_products'.split()

    def get_count_products(self, category):
        count = category.categories.count()
        return count

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields= 'text star'.split()

class ProductSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True)
    ave_rating=serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields= 'title description price reviews ave_rating'.split()

    def get_ave_rating(self,product):
        reviewss = product.reviews.all()
        if reviewss:
            sum_reviews = sum(i.star for i in reviewss)
            average = sum_reviews / len(reviewss)
            return round(average,1)
        return None


class ProductValidationSerializer(serializers.Serializer):
    title=serializers.CharField()
    price = serializers.IntegerField(min_value=1)
    description=serializers.CharField()
    category_id=serializers.IntegerField()

    def validate_category_id(self,category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Category does not exist")
        return category_id

class CategoryValidationSerializer(serializers.Serializer):
    name=serializers.CharField()

class ReviewValidationSerializer(serializers.Serializer):
    title=serializers.CharField()
    star=serializers.IntegerField(min_value=1)
    product_id=serializers.IntegerField()

    def validate_product_id(self,product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product does not exist")
        return product_id