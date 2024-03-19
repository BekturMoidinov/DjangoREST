from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    def __str__(self):
        return self.title



STARS=((star,star*'*') for star in range(1,6))
class Review(models.Model):
    text = models.TextField()
    star= models.IntegerField(choices=STARS,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    def __str__(self):
        return self.text





