"""
AI-Powered Outfit Recommendations Module
Uses OpenAI to generate intelligent outfit suggestions based on user's closet items.
"""

from openai import OpenAI
import os
from typing import List, Dict, Optional
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_outfit_recommendation(
    items: List[Dict],
    occasion: Optional[str] = None,
    weather: Optional[str] = None,
    style_preference: Optional[str] = None
) -> Dict:
    """
    Generate outfit recommendations using OpenAI based on available clothing items.
    
    Args:
        items: List of clothing items with their details
        occasion: Optional occasion type (casual, formal, business, etc.)
        weather: Optional weather condition (sunny, rainy, cold, etc.)
        style_preference: Optional style preference (minimalist, bold, classic, etc.)
    
    Returns:
        Dictionary containing outfit recommendations with reasoning
    """
    
    # Prepare item descriptions for AI
    item_descriptions = []
    for item in items:
        desc = f"- {item.get('category', 'Item')}"
        if item.get('color'):
            desc += f" in {item['color']}"
        if item.get('brand'):
            desc += f" by {item['brand']}"
        if item.get('notes'):
            desc += f" ({item['notes']})"
        item_descriptions.append(desc)
    
    # Build context for AI
    context = "Available clothing items:\n" + "\n".join(item_descriptions)
    
    # Build prompt
    prompt = f"""You are a professional fashion stylist. Based on the following clothing items, suggest 3 complete outfit combinations.

{context}

"""
    
    if occasion:
        prompt += f"\nOccasion: {occasion}"
    if weather:
        prompt += f"\nWeather: {weather}"
    if style_preference:
        prompt += f"\nStyle preference: {style_preference}"
    
    prompt += """

For each outfit, provide:
1. A list of items to combine
2. Why this combination works
3. Style tips for wearing it

Format your response as JSON with this structure:
{
  "outfits": [
    {
      "name": "Outfit name",
      "items": ["item1", "item2", "item3"],
      "reasoning": "Why this works",
      "style_tips": "How to wear it"
    }
  ]
}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional fashion stylist with expertise in creating stylish outfit combinations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse AI response
        ai_response = response.choices[0].message.content
        
        # Try to extract JSON from response
        try:
            # Find JSON in the response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = ai_response[start_idx:end_idx]
                recommendations = json.loads(json_str)
            else:
                recommendations = {"outfits": [], "raw_response": ai_response}
        except json.JSONDecodeError:
            recommendations = {"outfits": [], "raw_response": ai_response}
        
        return {
            "success": True,
            "recommendations": recommendations,
            "context": {
                "occasion": occasion,
                "weather": weather,
                "style_preference": style_preference,
                "items_count": len(items)
            }
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "recommendations": {"outfits": []}
        }


def analyze_closet_gaps(items: List[Dict]) -> Dict:
    """
    Analyze user's closet and suggest items they might be missing.
    
    Args:
        items: List of clothing items in user's closet
    
    Returns:
        Dictionary with gap analysis and suggestions
    """
    
    item_descriptions = []
    for item in items:
        desc = f"{item.get('category', 'Item')}"
        if item.get('color'):
            desc += f" ({item['color']})"
        item_descriptions.append(desc)
    
    prompt = f"""As a fashion consultant, analyze this wardrobe and identify gaps or missing essentials:

Current items:
{chr(10).join(['- ' + desc for desc in item_descriptions])}

Provide:
1. Essential items that are missing
2. Versatile pieces that would complement the existing wardrobe
3. Suggestions for building a more complete wardrobe

Format as JSON:
{{
  "missing_essentials": ["item1", "item2"],
  "recommended_additions": ["item1", "item2"],
  "wardrobe_analysis": "Overall assessment"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a fashion consultant specializing in wardrobe building."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content
        
        # Extract JSON
        try:
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = ai_response[start_idx:end_idx]
                analysis = json.loads(json_str)
            else:
                analysis = {"raw_response": ai_response}
        except json.JSONDecodeError:
            analysis = {"raw_response": ai_response}
        
        return {
            "success": True,
            "analysis": analysis
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_style_advice(item_description: str, user_context: Optional[str] = None) -> str:
    """
    Get styling advice for a specific item.
    
    Args:
        item_description: Description of the clothing item
        user_context: Optional context about user's style or occasion
    
    Returns:
        Styling advice as a string
    """
    
    prompt = f"Provide styling advice for: {item_description}"
    if user_context:
        prompt += f"\nContext: {user_context}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a fashion stylist providing practical styling advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Unable to generate styling advice: {str(e)}"
