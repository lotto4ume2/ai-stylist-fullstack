"""
Social Features Module
Handles outfit sharing, outfit planning, and social interactions.
"""

import uuid
import secrets
from typing import List, Dict, Optional
from datetime import date, datetime, timedelta


def generate_share_token() -> str:
    """Generate a unique share token for outfit sharing."""
    return secrets.token_urlsafe(16)


def create_shareable_outfit(
    user_id: str,
    outfit_name: str,
    item_ids: List[str],
    description: Optional[str] = None,
    is_public: bool = True
) -> Dict:
    """
    Create a shareable outfit link.
    
    Args:
        user_id: ID of the user creating the share
        outfit_name: Name of the outfit
        item_ids: List of clothing item IDs in the outfit
        description: Optional description
        is_public: Whether the outfit is publicly viewable
    
    Returns:
        Dictionary with share token and outfit details
    """
    
    share_token = generate_share_token()
    
    return {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "outfit_name": outfit_name,
        "item_ids": item_ids,
        "description": description,
        "share_token": share_token,
        "is_public": is_public,
        "view_count": 0,
        "created_at": datetime.utcnow().isoformat()
    }


def create_outfit_plan(
    user_id: str,
    outfit_name: str,
    item_ids: List[str],
    planned_date: Optional[date] = None,
    occasion: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict:
    """
    Create an outfit plan for a future date.
    
    Args:
        user_id: ID of the user
        outfit_name: Name of the outfit
        item_ids: List of clothing item IDs
        planned_date: Date when outfit is planned to be worn
        occasion: Occasion for the outfit
        notes: Additional notes
    
    Returns:
        Dictionary with outfit plan details
    """
    
    return {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "outfit_name": outfit_name,
        "item_ids": item_ids,
        "planned_date": planned_date.isoformat() if planned_date else None,
        "occasion": occasion,
        "notes": notes,
        "is_completed": False,
        "created_at": datetime.utcnow().isoformat()
    }


def get_upcoming_outfit_plans(outfit_plans: List[Dict], days_ahead: int = 7) -> List[Dict]:
    """
    Get outfit plans for the next N days.
    
    Args:
        outfit_plans: List of all outfit plans
        days_ahead: Number of days to look ahead
    
    Returns:
        Filtered list of upcoming outfit plans
    """
    
    today = date.today()
    future_date = today + timedelta(days=days_ahead)
    
    upcoming = []
    for plan in outfit_plans:
        if plan.get('planned_date'):
            try:
                plan_date = date.fromisoformat(plan['planned_date'])
                if today <= plan_date <= future_date and not plan.get('is_completed'):
                    upcoming.append(plan)
            except (ValueError, TypeError):
                continue
    
    # Sort by date
    upcoming.sort(key=lambda x: x.get('planned_date', ''))
    
    return upcoming


def record_outfit_worn(
    user_id: str,
    outfit_name: str,
    item_ids: List[str],
    worn_date: date,
    occasion: Optional[str] = None,
    weather: Optional[str] = None,
    rating: Optional[int] = None,
    notes: Optional[str] = None
) -> Dict:
    """
    Record that an outfit was worn.
    
    Args:
        user_id: ID of the user
        outfit_name: Name of the outfit
        item_ids: List of clothing item IDs
        worn_date: Date outfit was worn
        occasion: Occasion
        weather: Weather conditions
        rating: Rating from 1-5
        notes: Additional notes
    
    Returns:
        Dictionary with outfit history record
    """
    
    return {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "outfit_name": outfit_name,
        "item_ids": item_ids,
        "worn_date": worn_date.isoformat(),
        "occasion": occasion,
        "weather": weather,
        "rating": rating,
        "notes": notes,
        "created_at": datetime.utcnow().isoformat()
    }


def generate_outfit_inspiration(items: List[Dict], theme: Optional[str] = None) -> List[Dict]:
    """
    Generate outfit inspiration based on available items.
    
    Args:
        items: List of clothing items
        theme: Optional theme (e.g., "casual", "formal", "date night")
    
    Returns:
        List of suggested outfit combinations
    """
    
    # Group items by category
    categories = {}
    for item in items:
        category = item.get('category', 'other').lower()
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    # Generate simple combinations
    inspirations = []
    
    # Try to create complete outfits
    tops = categories.get('shirt', []) + categories.get('t-shirt', []) + categories.get('blouse', [])
    bottoms = categories.get('jeans', []) + categories.get('pants', []) + categories.get('skirt', [])
    shoes = categories.get('shoes', []) + categories.get('sneakers', []) + categories.get('boots', [])
    
    # Create combinations
    for top in tops[:3]:  # Limit to avoid too many combinations
        for bottom in bottoms[:3]:
            outfit = {
                "name": f"{top.get('color', '')} {top.get('category', 'top')} with {bottom.get('color', '')} {bottom.get('category', 'bottom')}",
                "items": [top['id'], bottom['id']],
                "theme": theme or "casual"
            }
            
            # Add shoes if available
            if shoes:
                outfit["items"].append(shoes[0]['id'])
            
            inspirations.append(outfit)
    
    return inspirations[:5]  # Return top 5 combinations
