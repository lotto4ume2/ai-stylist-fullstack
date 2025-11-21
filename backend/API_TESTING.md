# API Testing Guide

This guide provides examples for testing the AI-Stylist API endpoints using `curl` and Python.

## Prerequisites

- Backend server running on `http://localhost:8000`
- Supabase configured with credentials in `.env`

## Testing with curl

### 1. Health Check

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "AI-Stylist API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 2. User Signup

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "full_name": "Test User"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "uuid-here",
  "email": "test@example.com"
}
```

**Save the `access_token` for subsequent requests!**

### 3. User Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "uuid-here",
  "email": "test@example.com"
}
```

### 4. Upload Clothing Item

```bash
# Replace YOUR_TOKEN with the access_token from signup/login
# Replace /path/to/image.jpg with an actual image file

curl -X POST http://localhost:8000/api/items/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "category=shirt" \
  -F "color=blue" \
  -F "brand=Nike" \
  -F "notes=Favorite casual shirt"
```

**Expected Response:**
```json
{
  "message": "Clothing item uploaded successfully",
  "item": {
    "id": "uuid-here",
    "user_id": "user-uuid",
    "image_url": "https://xxx.supabase.co/storage/v1/object/public/clothing-items/...",
    "category": "shirt",
    "color": "blue",
    "brand": "Nike",
    "notes": "Favorite casual shirt",
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

### 5. Get All Clothing Items

```bash
curl -X GET http://localhost:8000/api/items \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**
```json
{
  "items": [
    {
      "id": "uuid-1",
      "user_id": "user-uuid",
      "image_url": "https://...",
      "category": "shirt",
      "color": "blue",
      "brand": "Nike",
      "notes": "Favorite casual shirt",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ],
  "count": 1
}
```

### 6. Delete Clothing Item

```bash
# Replace ITEM_ID with the actual item ID
curl -X DELETE http://localhost:8000/api/items/ITEM_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response:**
```json
{
  "message": "Item deleted successfully"
}
```

## Testing with Python

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    response = requests.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "full_name": "Test User"
        }
    )
    print("Signup Response:", response.status_code)
    data = response.json()
    print(json.dumps(data, indent=2))
    return data.get("access_token")

def test_login():
    """Test user login"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "SecurePassword123!"
        }
    )
    print("Login Response:", response.status_code)
    data = response.json()
    print(json.dumps(data, indent=2))
    return data.get("access_token")

def test_upload(token, image_path):
    """Test image upload"""
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        data = {
            "category": "shirt",
            "color": "blue",
            "brand": "Nike",
            "notes": "Test upload"
        }
        response = requests.post(
            f"{BASE_URL}/api/items/upload",
            headers=headers,
            files=files,
            data=data
        )
    
    print("Upload Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

def test_get_items(token):
    """Test getting all items"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/items",
        headers=headers
    )
    print("Get Items Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json().get("items", [])

def test_delete_item(token, item_id):
    """Test deleting an item"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        f"{BASE_URL}/api/items/{item_id}",
        headers=headers
    )
    print("Delete Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Test signup (or login if user exists)
    try:
        token = test_signup()
    except:
        token = test_login()
    
    # Test upload (replace with your image path)
    # test_upload(token, "/path/to/your/image.jpg")
    
    # Test getting items
    items = test_get_items(token)
    
    # Test delete (if items exist)
    if items:
        test_delete_item(token, items[0]["id"])
```

Run the test:
```bash
python3 test_api.py
```

## Testing with Postman

### Import Collection

Create a Postman collection with these requests:

1. **Signup**
   - Method: POST
   - URL: `http://localhost:8000/api/auth/signup`
   - Body (JSON):
     ```json
     {
       "email": "test@example.com",
       "password": "SecurePassword123!",
       "full_name": "Test User"
     }
     ```

2. **Login**
   - Method: POST
   - URL: `http://localhost:8000/api/auth/login`
   - Body (JSON):
     ```json
     {
       "email": "test@example.com",
       "password": "SecurePassword123!"
     }
     ```

3. **Upload Item**
   - Method: POST
   - URL: `http://localhost:8000/api/items/upload`
   - Headers: `Authorization: Bearer {{token}}`
   - Body (form-data):
     - `file`: (select image file)
     - `category`: shirt
     - `color`: blue
     - `brand`: Nike
     - `notes`: Test item

4. **Get Items**
   - Method: GET
   - URL: `http://localhost:8000/api/items`
   - Headers: `Authorization: Bearer {{token}}`

5. **Delete Item**
   - Method: DELETE
   - URL: `http://localhost:8000/api/items/{{item_id}}`
   - Headers: `Authorization: Bearer {{token}}`

### Environment Variables

Create a Postman environment with:
- `base_url`: `http://localhost:8000`
- `token`: (set after login)
- `item_id`: (set after getting items)

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```
**Solution**: Check that your token is valid and included in the Authorization header.

### 400 Bad Request (Signup)
```json
{
  "detail": "Signup failed: User already registered"
}
```
**Solution**: Use a different email or try logging in instead.

### 400 Bad Request (Upload)
```json
{
  "detail": "Invalid file type. Allowed types: image/jpeg, image/png, image/jpg, image/webp"
}
```
**Solution**: Ensure you're uploading a valid image file.

### 404 Not Found
```json
{
  "detail": "Item not found"
}
```
**Solution**: Check that the item ID exists and belongs to the authenticated user.

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser using these interfaces!

## Tips for Testing

1. **Use the interactive docs** at `/docs` for quick testing
2. **Save your token** after signup/login for subsequent requests
3. **Check Supabase dashboard** to verify data is being stored
4. **Use small test images** (< 1 MB) for faster uploads
5. **Test error cases** to ensure proper error handling
6. **Monitor server logs** for debugging information

## Next Steps

Once the API is working correctly:
1. Build the frontend to consume these endpoints
2. Test the full flow from UI to database
3. Prepare for deployment
