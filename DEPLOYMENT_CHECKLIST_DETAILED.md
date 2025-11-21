# AI-Stylist Deployment Checklist

Use this checklist to ensure you complete all deployment steps correctly.

---

## Pre-Deployment (Local)

### Backend Preparation
- [ ] Generate new production SECRET_KEY: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Save the SECRET_KEY somewhere safe (you'll need it for Render)
- [ ] Verify `requirements.txt` includes all dependencies
- [ ] Add `gunicorn==22.0.0` to `requirements.txt`
- [ ] Commit and push all changes to GitHub

### Frontend Preparation
- [ ] Test production build locally: `cd frontend && pnpm build && pnpm start`
- [ ] Verify no errors in the build
- [ ] Ensure `.env.local.example` exists for reference
- [ ] Commit and push all changes to GitHub

---

## Backend Deployment (Render)

### Account Setup
- [ ] Create Render account at https://render.com
- [ ] Verify email address
- [ ] Connect GitHub account to Render

### Service Creation
- [ ] Click "New +" → "Web Service"
- [ ] Connect your GitHub repository
- [ ] Configure service:
  - [ ] **Name**: `ai-stylist-backend`
  - [ ] **Region**: Choose closest region
  - [ ] **Branch**: `main`
  - [ ] **Root Directory**: `backend`
  - [ ] **Environment**: `Python 3`
  - [ ] **Build Command**: `pip install -r requirements.txt`
  - [ ] **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
  - [ ] **Instance Type**: `Free`

### Environment Variables
Add these in Render's "Advanced" section:

- [ ] `SUPABASE_URL` = `https://sovubmmohzuqmorvwdgn.supabase.co`
- [ ] `SUPABASE_KEY` = Your Supabase anon key
- [ ] `SUPABASE_SERVICE_KEY` = Your Supabase service_role key
- [ ] `SECRET_KEY` = The new key you generated
- [ ] `ENVIRONMENT` = `production`
- [ ] `PYTHON_VERSION` = `3.11.0`

### Deploy & Test
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes for deployment
- [ ] Copy your Render URL (e.g., `https://ai-stylist-backend.onrender.com`)
- [ ] Test health check: `curl https://your-backend-url.onrender.com/`
- [ ] Verify response: `{"message":"AI-Stylist API is running"...}`

---

## Frontend Deployment (Vercel)

### Account Setup
- [ ] Create Vercel account at https://vercel.com
- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Login to Vercel: `vercel login`

### Initial Deployment
- [ ] Navigate to frontend directory: `cd frontend`
- [ ] Start deployment: `vercel`
- [ ] Answer prompts:
  - [ ] Set up and deploy? → `Y`
  - [ ] Which scope? → Select your account
  - [ ] Link to existing project? → `N`
  - [ ] Project name? → `ai-stylist`
  - [ ] Directory? → `./`
  - [ ] Override settings? → `N`

### Environment Variables
- [ ] Link project: `vercel link`
- [ ] Add `NEXT_PUBLIC_API_URL`:
  ```bash
  vercel env add NEXT_PUBLIC_API_URL
  # Enter your Render URL
  # Select: Production, Preview, Development
  ```
- [ ] Add `NEXT_PUBLIC_SUPABASE_URL`:
  ```bash
  vercel env add NEXT_PUBLIC_SUPABASE_URL
  # Enter: https://sovubmmohzuqmorvwdgn.supabase.co
  # Select: Production, Preview, Development
  ```
- [ ] Add `NEXT_PUBLIC_SUPABASE_ANON_KEY`:
  ```bash
  vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
  # Enter your Supabase anon key
  # Select: Production, Preview, Development
  ```

### Production Deployment
- [ ] Deploy to production: `vercel --prod`
- [ ] Wait for deployment to complete
- [ ] Copy your Vercel URL (e.g., `https://ai-stylist.vercel.app`)

---

## Post-Deployment Configuration

### Update Backend CORS
- [ ] Open `backend/main.py`
- [ ] Add Vercel URL to origins list:
  ```python
  origins = [
      "http://localhost:3000",
      "https://ai-stylist.vercel.app"  # Your Vercel URL
  ]
  ```
- [ ] Commit and push to GitHub
- [ ] Wait for Render to auto-redeploy (check Render dashboard)

---

## Testing (Production)

### Functional Testing
- [ ] Visit your Vercel URL in browser
- [ ] Test Signup:
  - [ ] Click "Sign Up"
  - [ ] Enter email, password, full name
  - [ ] Verify redirect to /closet
  - [ ] Check browser localStorage for tokens
- [ ] Test Logout:
  - [ ] Click logout button
  - [ ] Verify redirect to home page
  - [ ] Check localStorage cleared
- [ ] Test Login:
  - [ ] Click "Login"
  - [ ] Enter credentials
  - [ ] Verify redirect to /closet
- [ ] Test Upload:
  - [ ] Navigate to /upload
  - [ ] Select image file
  - [ ] Fill in metadata (category, color, brand)
  - [ ] Click upload
  - [ ] Verify redirect to /closet
  - [ ] Confirm image appears
- [ ] Test Delete:
  - [ ] Click delete on an item
  - [ ] Verify item removed
  - [ ] Refresh page to confirm

### Cross-Browser Testing
- [ ] Test on Chrome
- [ ] Test on Firefox
- [ ] Test on Safari (if available)
- [ ] Test on Edge

### Mobile Testing
- [ ] Test on mobile browser (iOS/Android)
- [ ] Verify responsive design
- [ ] Test all user flows on mobile

### Performance Testing
- [ ] Check Vercel deployment logs for errors
- [ ] Check Render logs for backend errors
- [ ] Test page load speed
- [ ] Verify images load correctly

---

## Optional Enhancements

### Custom Domain
- [ ] Purchase domain from Namecheap/GoDaddy
- [ ] Add to Vercel: Settings → Domains
- [ ] Configure DNS records
- [ ] Update backend CORS with new domain

### Analytics
- [ ] Add Vercel Analytics: `pnpm add @vercel/analytics`
- [ ] Update `app/layout.tsx` with Analytics component
- [ ] Redeploy frontend

### Monitoring
- [ ] Set up Render health checks
- [ ] Configure Vercel deployment notifications
- [ ] Set up error tracking (Sentry, optional)

---

## Environment Variables Reference

### Backend (Render)
```env
SUPABASE_URL=https://sovubmmohzuqmorvwdgn.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvdnVibW1vaHp1cW1vcnZ3ZGduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzNjI2MzEsImV4cCI6MjA3ODkzODYzMX0.dTFeG4aCQJYoOa0c7j7vVIChG2QoB9E_SxQ34Md8vps
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvdnVibW1vaHp1cW1vcnZ3ZGduIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzM2MjYzMSwiZXhwIjoyMDc4OTM4NjMxfQ._NEx8vPinrtCEGk0wegJ4FN9-ymPauxoU6-UepEXYtY
SECRET_KEY=<YOUR_NEW_GENERATED_KEY>
ENVIRONMENT=production
PYTHON_VERSION=3.11.0
```

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
NEXT_PUBLIC_SUPABASE_URL=https://sovubmmohzuqmorvwdgn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvdnVibW1vaHp1cW1vcnZ3ZGduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzNjI2MzEsImV4cCI6MjA3ODkzODYzMX0.dTFeG4aCQJYoOa0c7j7vVIChG2QoB9E_SxQ34Md8vps
```

---

## Troubleshooting Guide

### Backend Issues

**Problem: Build fails on Render**
- [ ] Check Render logs for specific error
- [ ] Verify `requirements.txt` is complete
- [ ] Ensure Root Directory is set to `backend`
- [ ] Check Python version compatibility

**Problem: Backend returns 502 Bad Gateway**
- [ ] Check Start Command is correct
- [ ] Verify gunicorn is in requirements.txt
- [ ] Check Render logs for application errors
- [ ] Ensure environment variables are set

**Problem: Database connection fails**
- [ ] Verify SUPABASE_URL is correct
- [ ] Check SUPABASE_KEY and SUPABASE_SERVICE_KEY
- [ ] Test Supabase connection from Supabase dashboard
- [ ] Ensure database schema is created

### Frontend Issues

**Problem: Build fails on Vercel**
- [ ] Check Vercel build logs
- [ ] Verify all dependencies in package.json
- [ ] Test build locally: `pnpm build`
- [ ] Check for TypeScript errors

**Problem: 500 Internal Server Error**
- [ ] Check Vercel function logs
- [ ] Verify environment variables are set
- [ ] Check for localStorage SSR errors
- [ ] Ensure NEXT_PUBLIC_API_URL is correct

**Problem: CORS errors in browser**
- [ ] Verify Vercel URL in backend origins list
- [ ] Check backend has been redeployed
- [ ] Clear browser cache
- [ ] Check browser console for exact error

**Problem: "Failed to fetch" errors**
- [ ] Verify NEXT_PUBLIC_API_URL points to Render URL
- [ ] Check backend is running (visit /docs endpoint)
- [ ] Verify network connectivity
- [ ] Check browser console for details

### Authentication Issues

**Problem: Can't sign up**
- [ ] Check Supabase dashboard for errors
- [ ] Verify email format is valid
- [ ] Check backend logs for error details
- [ ] Ensure Supabase Auth is enabled

**Problem: Can't login**
- [ ] Verify credentials are correct
- [ ] Check Supabase Auth logs
- [ ] Ensure JWT SECRET_KEY is set
- [ ] Check backend authentication logic

**Problem: Session not persisting**
- [ ] Check localStorage in browser DevTools
- [ ] Verify token is being stored
- [ ] Check token expiration time
- [ ] Ensure auth context is working

---

## Success Criteria

Your deployment is successful when:

- ✅ Backend health check returns 200 OK
- ✅ Frontend loads without errors
- ✅ User can sign up successfully
- ✅ User can login successfully
- ✅ User can upload clothing items
- ✅ Images appear in digital closet
- ✅ User can delete items
- ✅ No CORS errors in browser console
- ✅ Mobile responsive design works
- ✅ All pages load within 3 seconds

---

## Post-Deployment Maintenance

### Weekly Tasks
- [ ] Check Render logs for errors
- [ ] Check Vercel analytics for usage
- [ ] Monitor Supabase storage usage
- [ ] Review user feedback (if any)

### Monthly Tasks
- [ ] Update dependencies
- [ ] Review security alerts
- [ ] Check for Render/Vercel updates
- [ ] Backup Supabase data

### As Needed
- [ ] Scale Render instance if traffic increases
- [ ] Upgrade Vercel plan if needed
- [ ] Add new features
- [ ] Fix bugs reported by users

---

## Estimated Time

- **Backend Deployment**: 20-30 minutes
- **Frontend Deployment**: 15-20 minutes
- **Testing**: 15-20 minutes
- **Total**: 50-70 minutes

---

## Support Resources

- **Render Documentation**: https://render.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **Supabase Documentation**: https://supabase.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com

---

**You're ready to deploy! Follow each step carefully and check off items as you complete them. Good luck! 🚀**
