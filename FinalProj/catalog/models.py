from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed, like description, image, etc.
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year_created = models.IntegerField()
    company = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)  # Add this line
    ratings = models.FloatField(default=0)  # Field to store ratings
    
                           
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']  # Define the default ordering


       
from django.contrib.auth.models import User

from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)  # You can use IntegerField for simplicity

    def __str__(self):
        return f"{self.user.username} - {self.item.name} - {self.rating}"

    class Meta:
        unique_together = ('item', 'user')
