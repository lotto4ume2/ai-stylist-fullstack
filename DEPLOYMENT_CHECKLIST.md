# Deployment Checklist

Use this checklist to deploy your AI-Stylist application to production.

## Pre-Deployment Checklist

### ✅ Supabase Setup

- [ ] Supabase project created
- [ ] Database schema executed (`schema.sql`)
- [ ] Storage bucket `clothing-items` created
- [ ] Storage bucket set to **public**
- [ ] Storage policies configured (upload, read, delete)
- [ ] Email confirmation disabled (for development) or configured (for production)
- [ ] API credentials saved (URL, anon key, service key)

### ✅ Backend Ready

- [ ] All dependencies in `requirements.txt`
- [ ] `.env.example` file created
- [ ] Code tested locally
- [ ] API endpoints working (test at `/docs`)
- [ ] Supabase connection working
- [ ] SECRET_KEY generated (strong random string)

### ✅ Frontend Ready

- [ ] All dependencies in `package.json`
- [ ] `.env.local.example` file created
- [ ] Code tested locally
- [ ] Build succeeds (`pnpm build`)
- [ ] All pages working
- [ ] Authentication flow tested

### ✅ Code Repository

- [ ] Code pushed to GitHub
- [ ] `.gitignore` configured
- [ ] No sensitive data in repository
- [ ] README files complete

---

## Backend Deployment (Choose One)

### Option A: Render

- [ ] Render account created
- [ ] New Web Service created
- [ ] GitHub repository connected
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables set:
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_KEY`
  - [ ] `SUPABASE_SERVICE_KEY`
  - [ ] `SECRET_KEY`
  - [ ] `ENVIRONMENT=production`
- [ ] Deployment successful
- [ ] Backend URL noted (e.g., `https://ai-stylist-backend.onrender.com`)
- [ ] Health check working (`/` endpoint)
- [ ] API docs accessible (`/docs`)

### Option B: Railway

- [ ] Railway account created
- [ ] Railway CLI installed
- [ ] Project initialized (`railway init`)
- [ ] Environment variables set
- [ ] Deployed (`railway up`)
- [ ] Domain obtained
- [ ] Backend tested

### Option C: Fly.io

- [ ] Fly.io account created
- [ ] Fly CLI installed
- [ ] `fly.toml` created
- [ ] Launched (`fly launch`)
- [ ] Secrets set
- [ ] Deployed (`fly deploy`)
- [ ] Backend tested

---

## Frontend Deployment (Choose One)

### Option A: Vercel (Recommended)

- [ ] Vercel account created
- [ ] New project created
- [ ] GitHub repository connected
- [ ] Root directory set to `frontend`
- [ ] Framework preset: Next.js (auto-detected)
- [ ] Environment variable set:
  - [ ] `NEXT_PUBLIC_API_URL` = your backend URL
- [ ] Deployment successful
- [ ] Frontend URL noted (e.g., `https://ai-stylist.vercel.app`)
- [ ] Landing page loads
- [ ] Can navigate to signup/login

### Option B: Netlify

- [ ] Netlify account created
- [ ] Site created from GitHub
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Deployed
- [ ] Frontend tested

---

## Post-Deployment Configuration

### Backend CORS Update

- [ ] Update `main.py` CORS settings with frontend URL:
  ```python
  allow_origins=[
      "http://localhost:3000",
      "https://your-frontend.vercel.app",  # Add this
  ]
  ```
- [ ] Commit and push changes
- [ ] Backend auto-deploys with new CORS settings

### Frontend Environment Update

- [ ] Verify `NEXT_PUBLIC_API_URL` points to production backend
- [ ] Redeploy if needed

---

## Testing in Production

### Authentication Flow

- [ ] Visit production frontend URL
- [ ] Click "Sign Up"
- [ ] Create test account
- [ ] Verify redirect to closet
- [ ] Logout
- [ ] Login with test account
- [ ] Verify redirect to closet

### Upload Flow

- [ ] Click "Add Item" or "Upload"
- [ ] Select test image
- [ ] Fill in metadata
- [ ] Upload item
- [ ] Verify item appears in closet
- [ ] Verify image loads correctly

### Delete Flow

- [ ] Click delete on test item
- [ ] Confirm deletion
- [ ] Verify item removed from closet

### Error Handling

- [ ] Test invalid login credentials
- [ ] Test duplicate signup email
- [ ] Test uploading invalid file type
- [ ] Test uploading oversized file
- [ ] Verify error messages display correctly

### Cross-Browser Testing

- [ ] Test on Chrome
- [ ] Test on Safari
- [ ] Test on Firefox
- [ ] Test on Edge

### Mobile Testing

- [ ] Test on mobile device or simulator
- [ ] Verify responsive design
- [ ] Test touch interactions

---

## Monitoring Setup

### Render

- [ ] Check deployment logs
- [ ] Set up log monitoring
- [ ] Check resource usage

### Vercel

- [ ] Enable Analytics (optional)
- [ ] Check deployment logs
- [ ] Set up error monitoring (optional)

### Supabase

- [ ] Check database usage
- [ ] Check storage usage
- [ ] Check bandwidth usage
- [ ] Verify within free tier limits

---

## Security Checklist

- [ ] All environment variables set correctly
- [ ] No secrets in code repository
- [ ] HTTPS enabled (automatic on Vercel/Render)
- [ ] CORS configured correctly
- [ ] Row Level Security enabled in Supabase
- [ ] Strong SECRET_KEY used
- [ ] Email confirmation enabled (for production)

---

## Performance Checklist

- [ ] Images loading quickly
- [ ] API responses fast (< 1 second)
- [ ] No console errors in browser
- [ ] Lighthouse score > 90 (optional)

---

## Documentation Checklist

- [ ] README.md complete
- [ ] GETTING_STARTED.md reviewed
- [ ] Deployment guides reviewed
- [ ] API documentation accessible

---

## Optional Enhancements

### Custom Domain

- [ ] Domain purchased
- [ ] DNS configured for frontend (Vercel)
- [ ] DNS configured for backend (Render)
- [ ] SSL certificates active

### Monitoring & Analytics

- [ ] Vercel Analytics enabled
- [ ] Error tracking set up (Sentry, etc.)
- [ ] Uptime monitoring configured

### CI/CD

- [ ] Auto-deploy on push to main
- [ ] Preview deployments for PRs
- [ ] Automated tests (if added)

---

## Troubleshooting

### Backend Issues

**Issue**: Deployment fails
- [ ] Check build logs in Render/Railway/Fly.io
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Check Python version compatibility

**Issue**: API not responding
- [ ] Check backend URL is correct
- [ ] Verify environment variables are set
- [ ] Check backend logs for errors

**Issue**: Database connection fails
- [ ] Verify Supabase credentials
- [ ] Check Supabase project is active
- [ ] Test connection from local environment

### Frontend Issues

**Issue**: Build fails
- [ ] Check build logs in Vercel
- [ ] Run `pnpm build` locally to reproduce
- [ ] Check for TypeScript errors

**Issue**: API calls failing
- [ ] Verify `NEXT_PUBLIC_API_URL` is correct
- [ ] Check backend CORS includes frontend URL
- [ ] Check browser console for errors

**Issue**: Images not loading
- [ ] Verify Supabase storage bucket is public
- [ ] Check storage policies
- [ ] Test image URLs directly in browser

---

## Success Criteria

Your deployment is successful when:

✅ Users can sign up and create accounts
✅ Users can login and logout
✅ Users can upload clothing images
✅ Images are stored and displayed correctly
✅ Users can view all their items
✅ Users can delete items
✅ Application works on mobile and desktop
✅ No errors in browser console
✅ API responds quickly (< 1 second)
✅ HTTPS is enabled
✅ Application is secure

---

## Next Steps After Deployment

1. **Share with friends** - Get feedback
2. **Monitor usage** - Check Supabase dashboard
3. **Add features** - Implement AI recommendations
4. **Optimize performance** - Improve load times
5. **Set up monitoring** - Track errors and uptime
6. **Create backups** - Regular database backups
7. **Plan scaling** - Prepare for more users

---

## Support Resources

- **Render Support**: https://render.com/docs
- **Vercel Support**: https://vercel.com/docs
- **Supabase Support**: https://supabase.com/docs
- **GitHub Issues**: Create issues in your repository

---

**Congratulations on deploying your application! 🚀**

You've successfully built and deployed a full-stack web application. This is a major achievement!
