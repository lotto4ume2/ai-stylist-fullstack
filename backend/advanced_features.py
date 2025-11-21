"""
Advanced Features Module
Handles favorites, outfit history, weather integration, and search functionality.
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, date
import os


def get_weather_recommendation(location: str = None, lat: float = None, lon: float = None) -> Dict:
    """
    Get weather-based clothing recommendations.
    Uses OpenWeatherMap API or similar service.
    
    Args:
        location: City name (e.g., "New York")
        lat: Latitude
        lon: Longitude
    
    Returns:
        Weather data with clothing recommendations
    """
    
    # For now, return mock data. In production, integrate with weather API
    # Example: OpenWeatherMap, WeatherAPI, etc.
    
    mock_weather = {
        "temperature": 72,
        "condition": "sunny",
        "humidity": 45,
        "wind_speed": 10,
        "recommendations": {
            "layers": "Light layers recommended",
            "accessories": ["sunglasses", "light jacket"],
            "avoid": ["heavy coats", "winter boots"],
            "suggested_categories": ["t-shirt", "jeans", "sneakers"]
        }
    }
    
    return {
        "success": True,
        "weather": mock_weather,
        "location": location or f"{lat},{lon}"
    }


def search_items(
    items: List[Dict],
    query: str = None,
    category: str = None,
    color: str = None,
    brand: str = None,
    tags: List[str] = None,
    is_favorite: bool = None
) -> List[Dict]:
    """
    Search and filter clothing items based on various criteria.
    
    Args:
        items: List of clothing items
        query: Text search query
        category: Filter by category
        color: Filter by color
        brand: Filter by brand
        tags: Filter by tags
        is_favorite: Filter favorites only
    
    Returns:
        Filtered list of items
    """
    
    filtered_items = items
    
    # Filter by favorite status
    if is_favorite is not None:
        filtered_items = [item for item in filtered_items if item.get('is_favorite') == is_favorite]
    
    # Filter by category
    if category:
        filtered_items = [item for item in filtered_items 
                         if item.get('category', '').lower() == category.lower()]
    
    # Filter by color
    if color:
        filtered_items = [item for item in filtered_items 
                         if item.get('color', '').lower() == color.lower()]
    
    # Filter by brand
    if brand:
        filtered_items = [item for item in filtered_items 
                         if item.get('brand', '').lower() == brand.lower()]
    
    # Filter by tags
    if tags:
        filtered_items = [item for item in filtered_items 
                         if any(tag in item.get('tags', []) for tag in tags)]
    
    # Text search in notes, category, color, brand
    if query:
        query_lower = query.lower()
        filtered_items = [
            item for item in filtered_items
            if query_lower in item.get('notes', '').lower() or
               query_lower in item.get('category', '').lower() or
               query_lower in item.get('color', '').lower() or
               query_lower in item.get('brand', '').lower()
        ]
    
    return filtered_items


def get_outfit_statistics(outfit_history: List[Dict]) -> Dict:
    """
    Generate statistics from outfit history.
    
    Args:
        outfit_history: List of worn outfits
    
    Returns:
        Statistics dictionary
    """
    
    if not outfit_history:
        return {
            "total_outfits": 0,
            "most_worn_items": [],
            "favorite_occasions": [],
            "average_rating": 0
        }
    
    # Calculate statistics
    total_outfits = len(outfit_history)
    
    # Count item usage
    item_usage = {}
    occasion_count = {}
    ratings = []
    
    for outfit in outfit_history:
        # Count items
        for item_id in outfit.get('item_ids', []):
            item_usage[item_id] = item_usage.get(item_id, 0) + 1
        
        # Count occasions
        occasion = outfit.get('occasion', 'casual')
        occasion_count[occasion] = occasion_count.get(occasion, 0) + 1
        
        # Collect ratings
        if outfit.get('rating'):
            ratings.append(outfit['rating'])
    
    # Get most worn items
    most_worn = sorted(item_usage.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Get favorite occasions
    favorite_occasions = sorted(occasion_count.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Calculate average rating
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return {
        "total_outfits": total_outfits,
        "most_worn_items": [{"item_id": item_id, "count": count} for item_id, count in most_worn],
        "favorite_occasions": [{"occasion": occ, "count": count} for occ, count in favorite_occasions],
        "average_rating": round(avg_rating, 2),
        "total_rated": len(ratings)
    }


def suggest_seasonal_items(current_season: str, items: List[Dict]) -> Dict:
    """
    Suggest appropriate items for the current season.
    
    Args:
        current_season: Current season (spring, summer, fall, winter)
        items: User's clothing items
    
    Returns:
        Seasonal recommendations
    """
    
    season_keywords = {
        "spring": ["light", "jacket", "cardigan", "jeans", "sneakers"],
        "summer": ["shorts", "t-shirt", "sandals", "dress", "tank"],
        "fall": ["sweater", "boots", "jeans", "jacket", "scarf"],
        "winter": ["coat", "boots", "sweater", "gloves", "hat"]
    }
    
    keywords = season_keywords.get(current_season.lower(), [])
    
    # Filter items that match seasonal keywords
    seasonal_items = []
    for item in items:
        item_text = f"{item.get('category', '')} {item.get('notes', '')}".lower()
        if any(keyword in item_text for keyword in keywords):
            seasonal_items.append(item)
    
    return {
        "season": current_season,
        "recommended_items": seasonal_items,
        "count": len(seasonal_items)
    }
