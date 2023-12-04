from django.contrib import admin
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # Customize other settings as needed

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'year_created', 'company', 'category')
    list_filter = ('category',)
    # Customize other settings as needed
