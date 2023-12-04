from catalog.models import Item

def recommend_similarly_priced_items(item_price, current_category):
    price_range = 200  # Define a price range for similarity
    min_price = item_price - price_range
    max_price = item_price + price_range
    recommended_items = Item.objects.filter(
        category__name__in=['Mouse', 'Keyboard', 'Monitor', 'Headset'],
        price__range=(min_price, max_price)
    ).exclude(category__name=current_category).order_by('price')[:4]

    print(recommended_items)  # Check what items are being fetched

    return recommended_items
