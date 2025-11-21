"""
AI-Stylist Backend API
A FastAPI application for managing user authentication and clothing item storage.
"""

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import os
from ai_recommendations import generate_outfit_recommendation, analyze_closet_gaps, get_style_advice
from advanced_features import get_weather_recommendation, search_items, get_outfit_statistics, suggest_seasonal_items
from social_features import create_shareable_outfit, create_outfit_plan, get_upcoming_outfit_plans, record_outfit_worn, generate_outfit_inspiration
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import uuid

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI-Stylist API",
    description="Backend API for AI-Stylist digital closet application",
    version="1.0.0"
)

# CORS configuration - will be updated with production URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()


# Pydantic models
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str


class ClothingItem(BaseModel):
    id: Optional[str] = None
    user_id: str
    image_url: str
    category: Optional[str] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None


class ClothingItemCreate(BaseModel):
    category: Optional[str] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    notes: Optional[str] = None


# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise credentials_exception


# API Routes
@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "AI-Stylist API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.post("/api/auth/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    """
    Register a new user account.
    
    This endpoint creates a new user in Supabase Auth and returns a JWT token.
    """
    try:
        # Sign up user with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "full_name": user.full_name
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user account"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": auth_response.user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=auth_response.user.id,
            email=user.email
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {str(e)}"
        )


@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin):
    """
    Authenticate user and return JWT token.
    
    This endpoint verifies user credentials and returns a JWT token for authenticated requests.
    """
    try:
        # Sign in with Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": auth_response.user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=auth_response.user.id,
            email=user.email
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )


@app.post("/api/items/upload")
async def upload_clothing_item(
    file: UploadFile = File(...),
    category: Optional[str] = None,
    color: Optional[str] = None,
    brand: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a clothing item image to the user's digital closet.
    
    This endpoint handles image upload to Supabase Storage and creates a database record.
    Requires JWT authentication.
    """
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Generate unique filename
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{current_user['user_id']}/{uuid.uuid4()}.{file_ext}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload to Supabase Storage
        storage_response = supabase.storage.from_("clothing-items").upload(
            unique_filename,
            file_content,
            {"content-type": file.content_type}
        )
        
        # Get public URL
        public_url = supabase.storage.from_("clothing-items").get_public_url(unique_filename)
        
        # Create database record
        item_data = {
            "id": str(uuid.uuid4()),
            "user_id": current_user["user_id"],
            "image_url": public_url,
            "category": category,
            "color": color,
            "brand": brand,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat()
        }
        
        db_response = supabase.table("clothing_items").insert(item_data).execute()
        
        return {
            "message": "Clothing item uploaded successfully",
            "item": db_response.data[0] if db_response.data else item_data
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@app.get("/api/items")
async def get_clothing_items(current_user: dict = Depends(get_current_user)):
    """
    Retrieve all clothing items for the authenticated user.
    
    Returns a list of all clothing items in the user's digital closet.
    """
    try:
        response = supabase.table("clothing_items").select("*").eq(
            "user_id", current_user["user_id"]
        ).order("created_at", desc=True).execute()
        
        return {
            "items": response.data,
            "count": len(response.data)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve items: {str(e)}"
        )


@app.delete("/api/items/{item_id}")
async def delete_clothing_item(item_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a clothing item from the user's digital closet.
    
    This endpoint removes both the database record and the image from storage.
    """
    try:
        # Get item to verify ownership and get image URL
        item_response = supabase.table("clothing_items").select("*").eq(
            "id", item_id
        ).eq("user_id", current_user["user_id"]).execute()
        
        if not item_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        item = item_response.data[0]
        
        # Extract filename from URL for storage deletion
        # URL format: https://{project}.supabase.co/storage/v1/object/public/clothing-items/{filename}
        image_url = item["image_url"]
        filename = image_url.split("/clothing-items/")[-1]
        
        # Delete from storage
        try:
            supabase.storage.from_("clothing-items").remove([filename])
        except:
            pass  # Continue even if storage deletion fails
        
        # Delete from database
        supabase.table("clothing_items").delete().eq("id", item_id).execute()
        
        return {"message": "Item deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete item: {str(e)}"
        )


@app.post("/api/recommendations/outfits")
async def get_outfit_recommendations(
    occasion: Optional[str] = None,
    weather: Optional[str] = None,
    style_preference: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get AI-powered outfit recommendations based on user's closet items.
    
    Requires JWT authentication.
    """
    try:
        # Get user's clothing items
        response = supabase.table("clothing_items").select("*").eq(
            "user_id", current_user["user_id"]
        ).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No clothing items found. Please add items to your closet first."
            )
        
        # Generate recommendations
        recommendations = generate_outfit_recommendation(
            items=response.data,
            occasion=occasion,
            weather=weather,
            style_preference=style_preference
        )
        
        return recommendations
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@app.post("/api/items/{item_id}/favorite")
async def toggle_favorite(item_id: str, current_user: dict = Depends(get_current_user)):
    """
    Toggle favorite status for a clothing item.
    """
    try:
        # Get current item
        item_response = supabase.table("clothing_items").select("*").eq(
            "id", item_id
        ).eq("user_id", current_user["user_id"]).execute()
        
        if not item_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        current_favorite = item_response.data[0].get('is_favorite', False)
        
        # Toggle favorite
        supabase.table("clothing_items").update({
            "is_favorite": not current_favorite
        }).eq("id", item_id).execute()
        
        return {
            "message": "Favorite status updated",
            "is_favorite": not current_favorite
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update favorite: {str(e)}"
        )


@app.get("/api/items/search")
async def search_clothing_items(
    query: Optional[str] = None,
    category: Optional[str] = None,
    color: Optional[str] = None,
    brand: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Search and filter clothing items.
    """
    try:
        # Get all user items
        response = supabase.table("clothing_items").select("*").eq(
            "user_id", current_user["user_id"]
        ).execute()
        
        # Apply filters
        filtered_items = search_items(
            items=response.data,
            query=query,
            category=category,
            color=color,
            brand=brand,
            is_favorite=is_favorite
        )
        
        return {
            "items": filtered_items,
            "count": len(filtered_items),
            "filters_applied": {
                "query": query,
                "category": category,
                "color": color,
                "brand": brand,
                "is_favorite": is_favorite
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@app.get("/api/weather/recommendations")
async def get_weather_based_recommendations(
    location: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get weather-based clothing recommendations.
    """
    try:
        weather_data = get_weather_recommendation(location=location)
        return weather_data
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get weather recommendations: {str(e)}"
        )


@app.get("/api/recommendations/closet-analysis")
async def analyze_closet(current_user: dict = Depends(get_current_user)):
    """
    Analyze user's closet and suggest missing items or gaps.
    
    Requires JWT authentication.
    """
    try:
        # Get user's clothing items
        response = supabase.table("clothing_items").select("*").eq(
            "user_id", current_user["user_id"]
        ).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No clothing items found. Please add items to your closet first."
            )
        
        # Analyze closet
        analysis = analyze_closet_gaps(response.data)
        
        return analysis
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze closet: {str(e)}"
        )


@app.post("/api/outfits/share")
async def share_outfit(
    outfit_name: str,
    item_ids: List[str],
    description: Optional[str] = None,
    is_public: bool = True,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a shareable outfit link.
    """
    try:
        # Create shareable outfit data
        outfit_data = create_shareable_outfit(
            user_id=current_user["user_id"],
            outfit_name=outfit_name,
            item_ids=item_ids,
            description=description,
            is_public=is_public
        )
        
        # Save to database
        db_response = supabase.table("shared_outfits").insert(outfit_data).execute()
        
        share_url = f"{SUPABASE_URL}/share/{outfit_data['share_token']}"
        
        return {
            "message": "Outfit shared successfully",
            "share_token": outfit_data['share_token'],
            "share_url": share_url,
            "outfit": db_response.data[0] if db_response.data else outfit_data
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to share outfit: {str(e)}"
        )


@app.get("/api/outfits/share/{share_token}")
async def get_shared_outfit(share_token: str):
    """
    Get a shared outfit by its token (public endpoint).
    """
    try:
        response = supabase.table("shared_outfits").select("*").eq(
            "share_token", share_token
        ).eq("is_public", True).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shared outfit not found"
            )
        
        # Increment view count
        supabase.table("shared_outfits").update({
            "view_count": response.data[0].get('view_count', 0) + 1
        }).eq("share_token", share_token).execute()
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve shared outfit: {str(e)}"
        )


@app.post("/api/outfits/plan")
async def plan_outfit(
    outfit_name: str,
    item_ids: List[str],
    planned_date: Optional[str] = None,
    occasion: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Create an outfit plan for a future date.
    """
    try:
        from datetime import date
        
        plan_date = None
        if planned_date:
            try:
                plan_date = date.fromisoformat(planned_date)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format. Use YYYY-MM-DD"
                )
        
        # Create outfit plan
        plan_data = create_outfit_plan(
            user_id=current_user["user_id"],
            outfit_name=outfit_name,
            item_ids=item_ids,
            planned_date=plan_date,
            occasion=occasion,
            notes=notes
        )
        
        # Save to database
        db_response = supabase.table("outfit_plans").insert(plan_data).execute()
        
        return {
            "message": "Outfit plan created successfully",
            "plan": db_response.data[0] if db_response.data else plan_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create outfit plan: {str(e)}"
        )


@app.get("/api/outfits/plans")
async def get_outfit_plans(current_user: dict = Depends(get_current_user)):
    """
    Get all outfit plans for the authenticated user.
    """
    try:
        response = supabase.table("outfit_plans").select("*").eq(
            "user_id", current_user["user_id"]
        ).order("planned_date", desc=False).execute()
        
        return {
            "plans": response.data,
            "count": len(response.data)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve outfit plans: {str(e)}"
        )


@app.get("/api/inspiration")
async def get_outfit_inspiration(
    theme: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get outfit inspiration based on user's closet.
    """
    try:
        # Get user's items
        response = supabase.table("clothing_items").select("*").eq(
            "user_id", current_user["user_id"]
        ).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No clothing items found. Add items to get inspiration!"
            )
        
        # Generate inspiration
        inspirations = generate_outfit_inspiration(response.data, theme=theme)
        
        return {
            "inspirations": inspirations,
            "count": len(inspirations),
            "theme": theme
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate inspiration: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
