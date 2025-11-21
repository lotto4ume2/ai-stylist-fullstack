# Frontend Deployment Guide

This guide covers deploying the AI-Stylist Next.js frontend to Vercel and other platforms.

## Deployment Options

1. **Vercel** (Recommended - Built by Next.js creators)
2. **Netlify** (Alternative with generous free tier)
3. **AWS Amplify** (AWS ecosystem)

---

## Option 1: Deploy to Vercel (Recommended)

Vercel is the best platform for Next.js applications, created by the same team.

### Prerequisites

- GitHub account
- Vercel account (sign up at https://vercel.com)
- Backend deployed and URL available
- Code pushed to GitHub repository

### Step 1: Prepare for Deployment

1. **Update `.env.local.example`** with production settings
2. **Ensure all dependencies** are in `package.json`
3. **Test build locally**:
   ```bash
   pnpm build
   ```

### Step 2: Deploy on Vercel

#### Method A: Using Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click **"Add New..."** → **"Project"**

2. **Import Git Repository**
   - Click **"Import Git Repository"**
   - Connect your GitHub account if not already connected
   - Select your `ai-stylist` repository
   - Click **"Import"**

3. **Configure Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `pnpm build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)
   - **Install Command**: `pnpm install` (auto-detected)

4. **Set Environment Variables**
   
   Click **"Environment Variables"** and add:
   
   | Name | Value |
   |------|-------|
   | `NEXT_PUBLIC_API_URL` | Your deployed backend URL (e.g., `https://ai-stylist-backend.onrender.com`) |

   **Important**: Make sure there's no trailing slash in the URL!

5. **Deploy**
   - Click **"Deploy"**
   - Wait 2-3 minutes for deployment
   - You'll get a URL like: `https://ai-stylist-xyz.vercel.app`

#### Method B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? ai-stylist-frontend
# - Directory? ./
# - Override settings? No

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL

# Enter your backend URL when prompted

# Deploy to production
vercel --prod
```

### Step 3: Update Backend CORS

After getting your Vercel URL, update the backend's CORS settings:

In `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy the backend after this change.

### Step 4: Test Your Deployment

1. Visit your Vercel URL
2. Test signup/login functionality
3. Upload a test image
4. Verify items appear in the closet

---

## Option 2: Deploy to Netlify

### Step 1: Create `netlify.toml`

Create `frontend/netlify.toml`:

```toml
[build]
  base = "frontend"
  command = "pnpm build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"

[build.environment]
  NODE_VERSION = "20"
```

### Step 2: Deploy

1. **Go to Netlify Dashboard**
   - Visit https://app.netlify.com
   - Click **"Add new site"** → **"Import an existing project"**

2. **Connect Repository**
   - Choose GitHub
   - Select your repository
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: `pnpm build`
     - **Publish directory**: `frontend/.next`

3. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add `NEXT_PUBLIC_API_URL` with your backend URL

4. **Deploy**
   - Click **"Deploy site"**

---

## Option 3: Deploy to AWS Amplify

### Step 1: Create `amplify.yml`

Create `frontend/amplify.yml`:

```yaml
version: 1
applications:
  - frontend:
      phases:
        preBuild:
          commands:
            - npm install -g pnpm
            - pnpm install
        build:
          commands:
            - pnpm build
      artifacts:
        baseDirectory: .next
        files:
          - '**/*'
      cache:
        paths:
          - node_modules/**/*
      buildPath: /frontend
```

### Step 2: Deploy

1. Go to AWS Amplify Console
2. Click **"New app"** → **"Host web app"**
3. Connect your GitHub repository
4. Select the `frontend` directory
5. Add environment variables
6. Deploy

---

## Custom Domain Setup

### Vercel

1. Go to your project settings
2. Click **"Domains"**
3. Add your custom domain
4. Update DNS records as instructed by Vercel

### Netlify

1. Go to **Domain settings**
2. Click **"Add custom domain"**
3. Follow DNS configuration instructions

---

## Environment Variables Management

### Production Environment Variables

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Vercel Environment Variables

You can set different values for:
- **Production**: Used for `vercel --prod`
- **Preview**: Used for PR deployments
- **Development**: Used locally

---

## Continuous Deployment

### Automatic Deployments

Vercel automatically deploys:
- **Production**: Every push to `main` branch
- **Preview**: Every pull request

### Preview Deployments

Every PR gets a unique preview URL:
```
https://ai-stylist-git-feature-branch.vercel.app
```

This is perfect for testing before merging!

---

## Performance Optimization

### Image Optimization

Next.js automatically optimizes images. For best performance:

```tsx
import Image from 'next/image';

<Image
  src={item.image_url}
  alt="Clothing item"
  width={400}
  height={400}
  className="object-cover"
/>
```

### Caching

Vercel automatically caches:
- Static assets
- API responses (with proper headers)
- Images

### Analytics

Enable Vercel Analytics:
1. Go to project settings
2. Click **"Analytics"**
3. Enable **"Web Analytics"**

---

## Monitoring and Debugging

### View Deployment Logs

**Vercel Dashboard:**
- Go to Deployments
- Click on a deployment
- View build logs and runtime logs

**Vercel CLI:**
```bash
vercel logs
```

### Common Issues

#### Issue: "Module not found"

**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules .next
pnpm install
pnpm build
```

#### Issue: Environment variables not working

**Solution:**
- Ensure variable name starts with `NEXT_PUBLIC_`
- Redeploy after adding variables
- Check variable is set in correct environment (Production/Preview)

#### Issue: API calls failing

**Solution:**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend CORS settings include frontend URL
- Test backend endpoint directly

#### Issue: Build fails

**Solution:**
- Check build logs for specific error
- Test build locally: `pnpm build`
- Ensure all dependencies are in `package.json`

---

## Security Best Practices

✓ **Use HTTPS** (automatic on Vercel)
✓ **Never commit** `.env.local` to Git
✓ **Use environment variables** for all API URLs
✓ **Enable security headers** in `next.config.js`
✓ **Keep dependencies updated**

### Security Headers

Add to `next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

---

## Rollback Deployments

### Vercel

1. Go to **Deployments**
2. Find the working deployment
3. Click **"..."** → **"Promote to Production"**

### Vercel CLI

```bash
vercel rollback
```

---

## Cost Considerations

### Vercel Free Tier

- **Bandwidth**: 100 GB/month
- **Serverless Function Execution**: 100 GB-hours
- **Deployments**: Unlimited
- **Team Members**: 1

### When to Upgrade

Upgrade to Pro ($20/month) when you need:
- More bandwidth
- Team collaboration
- Advanced analytics
- Priority support

---

## Testing Before Deployment

### Local Production Build

```bash
# Build for production
pnpm build

# Start production server
pnpm start

# Test at http://localhost:3000
```

### Environment-Specific Testing

```bash
# Test with production API
NEXT_PUBLIC_API_URL=https://your-backend.com pnpm dev
```

---

## Post-Deployment Checklist

✓ **Test signup/login** on production
✓ **Upload test images** to verify storage
✓ **Check responsive design** on mobile
✓ **Test all navigation** links
✓ **Verify error handling** works
✓ **Check loading states** display correctly
✓ **Test logout** functionality
✓ **Verify protected routes** redirect to login
✓ **Check browser console** for errors
✓ **Test on different browsers** (Chrome, Safari, Firefox)

---

## Next Steps

1. Deploy frontend to Vercel
2. Update backend CORS with frontend URL
3. Test complete user flow
4. Set up custom domain (optional)
5. Enable analytics and monitoring
6. Share with users!

---

## Support and Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **Vercel Community**: https://github.com/vercel/vercel/discussions
