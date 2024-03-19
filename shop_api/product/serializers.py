from rest_framework import serializers
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
            return average
        return None


