# Import statements
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Item
from .recommendation import recommend_similarly_priced_items
from django.db import models

# Views

import json

def index(request):
    if request.user.is_authenticated:
        all_items = Item.objects.all()
        all_items_json = json.dumps(list(all_items.values('id', 'ratings')))
        recently_viewed_ids = request.session.get('recently_viewed', [])[-3:]
        recently_viewed_items = [
            get_object_or_404(Item, id=item_id) for item_id in recently_viewed_ids
        ]
        return render(
            request,
            'catalog/index.html',
            {'all_items': all_items, 'recently_viewed_items': recently_viewed_items, 'all_items_json': all_items_json}
        )
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    recently_viewed = request.session.get('recently_viewed', [])
    category = item.category.name
    item_rating = Rating.objects.filter(item=item).aggregate(models.Avg('rating'))['rating__avg'] or 0

    if item_id not in recently_viewed:
        recently_viewed.insert(0, item_id)
        recently_viewed = recently_viewed[:3]
        request.session['recently_viewed'] = recently_viewed
    
    recommended_items = recommend_similarly_priced_items(item.price, category)
    print(recommended_items)  # Check if recommended_items has data
    
    return render(
        request,
        'catalog/item_detail.html',
        {'item': item, 'item_rating': item_rating, 'recommended_items': recommended_items}
    )

# Function related to recommendation

def recommend_similarly_priced_items(item_price, current_category):
    price_range = 20
    min_price = item_price - price_range
    max_price = item_price + price_range

    recommended_items = Item.objects.filter(
        category__name__in=['Mouse', 'Keyboard', 'Monitor', 'Headset'],
        price__range=(min_price, max_price)
    ).exclude(category__name=current_category).order_by('price')[:3]

    return recommended_items

# Additional function

def get_item_by_id_from_database(item_id):
    return get_object_or_404(Item, id=item_id)


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Item, Rating

from .models import Rating

@login_required
def rate_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)
        rating_value = request.POST.get('rating')  # Extract rating from the POST data
        
        # Create or update the rating for the user and item
        rating, created = Rating.objects.get_or_create(user=request.user, item=item)
        rating.rating = rating_value  # Ensure this matches the field name in your model
        rating.save()
        
        # Calculate average rating for the item
        item_ratings = Rating.objects.filter(item=item).values_list('rating', flat=True)
        avg_rating = sum(item_ratings) / len(item_ratings) if item_ratings else 0
        
        # Update the item's overall rating
        item.ratings = avg_rating
        item.save()
        
        return JsonResponse({'message': 'Success', 'new_rating': avg_rating})
    return JsonResponse({'message': 'Error'})


from django.http import JsonResponse

def get_ratings(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item_rating = Rating.objects.filter(item=item).aggregate(models.Avg('rating'))['rating__avg'] or 0
    return JsonResponse({'rating': item_rating})

from django.http import JsonResponse

def update_rating(request, item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        item = get_object_or_404(Item, pk=item_id)
        user_rating = request.POST.get('rating')
        
        # Create or update the rating for the user and item
        rating, created = Rating.objects.get_or_create(user=request.user, item=item)
        rating.rating = user_rating
        rating.save()
        
        # Update the average rating for the item based on all ratings
        all_ratings = Rating.objects.filter(item=item)
        item.ratings = all_ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        item.save()
        
        return JsonResponse({'message': 'Success', 'new_rating': item.ratings})
    return JsonResponse({'message': 'Error'})


