# AI Stylist - Quick Start Guide

## Your Environment Variables

Copy these values when deploying:

### Supabase Configuration
```
SUPABASE_URL=https://sovubmmohzuqmorvwdgn.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvdnVibW1vaHp1cW1vcnZ3ZGduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzNjI2MzEsImV4cCI6MjA3ODkzODYzMX0.dTFeG4aCQJYoOa0c7j7vVIChG2QoB9E_SxQ34Md8vps
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvdnVibW1vaHp1cW1vcnZ3ZGduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzM2MjYzMSwiZXhwIjoyMDc4OTM4NjMxfQ._NEx8vPinrtCEGk0wegJ4FN9-ymPauxoU6-UepEXYtY
```

### Backend Configuration
```
SECRET_KEY=owC14Zoh9lHA7EjrJX1FxoAAJbJwmn5DedFzE3ZSyhs
ENVIRONMENT=production
```

## Deployment Steps

### 1. Backend Deployment

**Choose ONE platform:**

- **Render**: Use `render.yaml` (easiest, requires card verification)
- **Fly.io**: Use `backend/fly.toml` and `flyctl` CLI
- **Railway**: Use `backend/railway.json`

### 2. Frontend Deployment

**Vercel** (recommended):
1. Connect your GitHub repository
2. Set Root Directory to `frontend`
3. Add environment variable: `NEXT_PUBLIC_BACKEND_URL` = your backend URL

### 3. Update CORS

After frontend deployment, update your backend's CORS settings to include the frontend URL.

## Repository

Your code is at: https://github.com/lotto4ume2/ai-stylist-fullstack

## Need Help?

See `DEPLOYMENT_GUIDE.md` for detailed instructions for each platform.
