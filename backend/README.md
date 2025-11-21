# AI-Stylist Backend API

FastAPI backend for the AI-Stylist digital closet application with Supabase authentication and storage.

## Features

- **User Authentication**: Secure signup and login with JWT tokens
- **Image Upload**: Upload clothing items to Supabase Storage
- **Digital Closet**: Store and retrieve clothing item metadata
- **RESTful API**: Clean, documented API endpoints
- **CORS Support**: Configured for frontend integration

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Supabase**: Backend-as-a-Service for authentication and storage
- **JWT**: Secure token-based authentication
- **Python 3.11**: Latest Python features and performance

## Prerequisites

- Python 3.11 or higher
- Supabase account and project
- pip package manager

## Installation

1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Supabase credentials:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon/public key
   - `SUPABASE_SERVICE_KEY`: Your Supabase service role key
   - `SECRET_KEY`: Generate a secure random string for JWT signing

3. **Generate a secure SECRET_KEY**:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

## Running the Server

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token

### Clothing Items

- `POST /api/items/upload` - Upload a clothing item (requires authentication)
- `GET /api/items` - Get all clothing items for authenticated user
- `DELETE /api/items/{item_id}` - Delete a clothing item

### Health Check

- `GET /` - API health check

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Project Structure

```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variable template
├── .env                # Your environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase anon/public key | Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | Yes |
| `SECRET_KEY` | JWT signing secret | Yes |
| `ENVIRONMENT` | development/production | No |

## Security Notes

- Never commit `.env` file to version control
- Use strong, randomly generated `SECRET_KEY`
- Keep `SUPABASE_SERVICE_KEY` secure
- Update CORS origins in production
- Use HTTPS in production

## Deployment

See the main project README for deployment instructions to Render, Railway, or other cloud providers.

## Future Enhancements

- AI outfit recommendation engine
- Image analysis for automatic categorization
- Outfit creation and management
- Social sharing features
- Integration with e-commerce platforms
