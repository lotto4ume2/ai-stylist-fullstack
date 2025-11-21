# Backend Deployment Guide

This guide covers deploying the AI-Stylist FastAPI backend to various cloud platforms.

## Deployment Options

1. **Render** (Recommended for beginners - Free tier available)
2. **Railway** (Easy deployment - Free tier available)
3. **Fly.io** (Good performance - Free tier available)
4. **AWS/GCP/Azure** (Production-grade - Paid)

---

## Option 1: Deploy to Render (Recommended)

Render offers a free tier and is very beginner-friendly.

### Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- Code pushed to GitHub repository

### Step 1: Prepare for Deployment

1. **Create `render.yaml`** (already created in the project)
2. **Ensure all dependencies** are in `requirements.txt`
3. **Push code to GitHub**

### Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click **"New +"** → **"Web Service"**

2. **Connect GitHub Repository**
   - Click **"Connect account"** to link your GitHub
   - Select your `ai-stylist` repository
   - Click **"Connect"**

3. **Configure Web Service**
   - **Name**: `ai-stylist-backend` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   
   Click **"Advanced"** → **"Add Environment Variable"** and add:
   
   | Key | Value |
   |-----|-------|
   | `SUPABASE_URL` | Your Supabase project URL |
   | `SUPABASE_KEY` | Your Supabase anon key |
   | `SUPABASE_SERVICE_KEY` | Your Supabase service role key |
   | `SECRET_KEY` | Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
   | `ENVIRONMENT` | `production` |

5. **Choose Plan**
   - Select **"Free"** for testing
   - Click **"Create Web Service"**

6. **Wait for Deployment**
   - Render will build and deploy your app (2-5 minutes)
   - You'll get a URL like: `https://ai-stylist-backend.onrender.com`

### Step 3: Update CORS Settings

After deployment, update `main.py` to include your Render URL in CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-url.vercel.app",  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push the changes. Render will auto-deploy.

### Step 4: Test Your Deployment

Visit your Render URL:
```
https://your-app-name.onrender.com/
```

You should see:
```json
{
  "message": "AI-Stylist API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

Check the API docs:
```
https://your-app-name.onrender.com/docs
```

---

## Option 2: Deploy to Railway

Railway is another excellent option with a generous free tier.

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Initialize Project

```bash
cd backend
railway init
```

### Step 4: Add Environment Variables

```bash
railway variables set SUPABASE_URL=your-supabase-url
railway variables set SUPABASE_KEY=your-supabase-key
railway variables set SUPABASE_SERVICE_KEY=your-service-key
railway variables set SECRET_KEY=your-secret-key
railway variables set ENVIRONMENT=production
```

### Step 5: Deploy

```bash
railway up
```

Railway will automatically detect Python and deploy your app.

### Step 6: Get Your URL

```bash
railway domain
```

---

## Option 3: Deploy to Fly.io

### Step 1: Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login

```bash
fly auth login
```

### Step 3: Create `fly.toml`

Create `backend/fly.toml`:

```toml
app = "ai-stylist-backend"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Step 4: Launch

```bash
cd backend
fly launch
```

### Step 5: Set Secrets

```bash
fly secrets set SUPABASE_URL=your-url
fly secrets set SUPABASE_KEY=your-key
fly secrets set SUPABASE_SERVICE_KEY=your-service-key
fly secrets set SECRET_KEY=your-secret-key
```

### Step 6: Deploy

```bash
fly deploy
```

---

## Post-Deployment Checklist

✓ **Test all endpoints** using the `/docs` interface
✓ **Verify Supabase connection** by creating a test user
✓ **Update frontend** with the new backend URL
✓ **Enable HTTPS** (should be automatic on all platforms)
✓ **Monitor logs** for any errors
✓ **Set up custom domain** (optional)

---

## Monitoring and Logs

### Render
```bash
# View logs in dashboard or CLI
render logs
```

### Railway
```bash
railway logs
```

### Fly.io
```bash
fly logs
```

---

## Troubleshooting

### Issue: "Application failed to start"

**Check:**
- Build command is correct
- Start command includes `--host 0.0.0.0`
- Port is set correctly (`$PORT` for Render/Railway)

### Issue: "Module not found"

**Solution:**
- Ensure all dependencies are in `requirements.txt`
- Rebuild the application

### Issue: "Database connection failed"

**Solution:**
- Verify Supabase environment variables are set correctly
- Check Supabase dashboard for connection issues

### Issue: CORS errors

**Solution:**
- Add your frontend URL to CORS origins in `main.py`
- Redeploy after making changes

---

## Scaling and Performance

### Free Tier Limitations

- **Render**: Spins down after 15 minutes of inactivity
- **Railway**: 500 hours/month, $5 credit
- **Fly.io**: 3 shared-cpu VMs

### Upgrade Recommendations

For production with consistent traffic:
- Upgrade to paid tier ($7-10/month)
- Enable auto-scaling
- Add monitoring and alerts
- Set up database backups

---

## Security Best Practices

✓ **Use environment variables** for all secrets
✓ **Enable HTTPS** (automatic on most platforms)
✓ **Rotate SECRET_KEY** regularly
✓ **Monitor API usage** for suspicious activity
✓ **Set up rate limiting** for production
✓ **Keep dependencies updated**

---

## Custom Domain Setup

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

### Railway
```bash
railway domain add yourdomain.com
```

### Fly.io
```bash
fly certs add yourdomain.com
```

---

## Continuous Deployment

All platforms support automatic deployment from GitHub:

1. **Connect your GitHub repository**
2. **Select branch** (e.g., `main`)
3. **Enable auto-deploy**

Now every push to the branch will trigger a new deployment!

---

## Next Steps

1. Deploy the backend using one of the methods above
2. Note your backend URL
3. Update frontend environment variables
4. Deploy the frontend (see frontend/DEPLOYMENT.md)
5. Test the full application end-to-end
