# AI-Stylist: Complete Deployment Guide

**Author**: Manus AI  
**Date**: November 21, 2025  
**Status**: ✅ Ready for Production Deployment

---

## Introduction

This guide provides comprehensive, step-by-step instructions for deploying your AI-Stylist application to production. We will deploy the **backend (FastAPI)** to **Render** and the **frontend (Next.js)** to **Vercel**. Both platforms offer generous free tiers that are perfect for this project.

**By the end of this guide, you will have a live, publicly accessible web application.**

### Prerequisites

Before you begin, ensure you have the following:

1.  **GitHub Account**: Your project code should be in a GitHub repository.
2.  **Render Account**: Sign up for free at [render.com](https://render.com).
3.  **Vercel Account**: Sign up for free at [vercel.com](https://vercel.com).
4.  **Node.js & pnpm**: Installed on your local machine for final checks.
5.  **Vercel CLI**: Install globally by running `npm install -g vercel`.

---

## Part 1: Backend Deployment to Render

We will start by deploying the FastAPI backend. Once it's live, we will have a URL to provide to our frontend.

### Step 1: Prepare Your Backend Code

**1.A: Generate a Production Secret Key**

Your JWT secret key in `.env` is for development only. Create a new, cryptographically secure key for production:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output. You will use this in the Render environment variables. **Do not commit this key to your `.env` file or GitHub.**

**1.B: Update CORS Origins**

For security, your backend will only accept requests from your frontend's domain. Since you don't have the Vercel URL yet, we'll add it later. For now, ensure your `backend/main.py` is ready:

```python
# backend/main.py (lines 30-36)

# We will update this list after deploying the frontend
origins = [
    "http://localhost:3000",
    # "https://your-frontend-url.vercel.app" will be added later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**1.C: Finalize `requirements.txt`**

Ensure your `backend/requirements.txt` file is complete and pushed to GitHub. It should look like this:

```txt
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
supabase==2.0.3
python-jose==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
email-validator==2.3.0
gunicorn==22.0.0
```
*Note: We've added `gunicorn` as it's a production-grade web server that Render works well with.*

### Step 2: Create a New Web Service on Render

1.  **Log in to your Render dashboard.**
2.  Click the **New +** button and select **Web Service**.

    *Screenshot Description: The Render dashboard with a prominent "New +" button in the top navigation bar. A dropdown menu appears, showing options like "Web Service", "Static Site", and "Database". The "Web Service" option is highlighted.*

3.  **Connect Your Repository**: Choose "Build and deploy from a Git repository" and connect the GitHub repository containing your `ai-stylist` project.

### Step 3: Configure the Render Service

Fill out the configuration form with the following settings:

-   **Name**: `ai-stylist-backend` (or a unique name of your choice).
-   **Region**: Choose a region close to you (e.g., Ohio, USA).
-   **Branch**: `main` (or your primary development branch).
-   **Root Directory**: `backend` (This is crucial! It tells Render to look inside your `backend` folder).
-   **Environment**: `Python 3`
-   **Build Command**: `pip install -r requirements.txt`
-   **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
-   **Instance Type**: `Free`

    *Screenshot Description: The Render service configuration page. Fields for "Name", "Region", "Branch", "Root Directory", "Build Command", and "Start Command" are filled out with the exact values listed above. The "Free" instance type is selected.*

### Step 4: Add Environment Variables

This is the most critical step for connecting your backend to Supabase.

1.  Scroll down to the **Advanced** section.
2.  Click **Add Environment Variable**.
3.  Add the following key-value pairs. The values should come from your Supabase project dashboard and the secret key you generated earlier.

| Key | Value |
| :--- | :--- |
| `SUPABASE_URL` | `https://sovubmmohzuqmorvwdgn.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (your anon key) |
| `SUPABASE_SERVICE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (your service_role key) |
| `SECRET_KEY` | The new secure key you generated in Step 1.A |
| `ENVIRONMENT` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

    *Screenshot Description: The "Environment Variables" section in Render's advanced settings. A table shows the keys and their corresponding (masked) values being added one by one.*

### Step 5: Deploy!

1.  Scroll to the bottom and click **Create Web Service**.
2.  Render will now start building and deploying your backend. This may take 5-10 minutes.
3.  You can monitor the progress in the **Logs** tab.
4.  Once deployed, Render will provide you with a public URL at the top of the page (e.g., `https://ai-stylist-backend.onrender.com`).

**Copy this URL! You will need it for the frontend.**

### Step 6: Test the Deployed Backend

Open a terminal and run a `curl` command to test the health check endpoint:

```bash
curl https://your-backend-url.onrender.com/
```

**Expected Output:**
```json
{"message":"AI-Stylist API is running","version":"1.0.0","status":"healthy"}
```

If you see this, your backend is live and working correctly!

---

## Part 2: Frontend Deployment to Vercel

With the backend live, we can now deploy the frontend and connect it to the production API.

### Step 1: Prepare Your Frontend Code

In your local `frontend` directory, you don't need to change any code. The environment variables will be handled by Vercel's system.

### Step 2: Deploy with Vercel CLI

1.  Open your terminal and navigate to the `frontend` directory:
    ```bash
    cd /path/to/your/project/frontend
    ```
2.  Log in to your Vercel account:
    ```bash
    vercel login
    ```
3.  Start the deployment process:
    ```bash
    vercel
    ```

4.  **Follow the CLI prompts:**
    -   **Set up and deploy?** `Y`
    -   **Which scope?** Choose your account (press Enter).
    -   **Link to existing project?** `N`
    -   **What's your project's name?** `ai-stylist` (press Enter).
    -   **In which directory is your code located?** `./` (press Enter).
    -   **Auto-detected settings:** Vercel will correctly identify it as a Next.js project. Don't override the settings.

    Vercel will now deploy a preview version of your site.

### Step 3: Add Environment Variables to Vercel

This step connects your frontend to your live backend and Supabase.

1.  **Link the local project to the Vercel project:**
    ```bash
    vercel link
    ```

2.  **Add the environment variables:**

    ```bash
    # Add the backend URL you copied from Render
    vercel env add NEXT_PUBLIC_API_URL
    # Paste your Render URL when prompted

    # Add your Supabase URL
    vercel env add NEXT_PUBLIC_SUPABASE_URL
    # Paste your Supabase URL when prompted

    # Add your Supabase Anon Key
    vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
    # Paste your Supabase anon key when prompted
    ```

    When asked which environments to add them to (Production, Preview, Development), select **all three**.

### Step 4: Deploy to Production

Now that your environment variables are set, push a final deployment to production:

```bash
vercel --prod
```

Vercel will build and deploy your site, making it live at your production URL (e.g., `https://ai-stylist.vercel.app`).

### Step 5: Final Backend Update (CORS)

1.  Go back to your `backend/main.py` file.
2.  Add your new Vercel production URL to the `origins` list.

    ```python
    origins = [
        "http://localhost:3000",
        "https://ai-stylist.vercel.app"  # Add your Vercel URL here!
    ]
    ```

3.  Commit and push this change to your GitHub repository.
4.  Render will automatically detect the push and redeploy your backend with the updated CORS policy.

---

## Part 3: Final Testing

Your application is now live! It's time to test it end-to-end.

1.  **Visit your Vercel URL** (e.g., `https://ai-stylist.vercel.app`).
2.  **Test Signup**: Create a new account with a real email address.
3.  **Test Login**: Log out and log back in.
4.  **Test Upload**: Upload a clothing item image.
5.  **Test Closet**: Verify the item appears in your digital closet.
6.  **Test Delete**: Delete the item and confirm it's gone.
7.  **Mobile Test**: Open the URL on your smartphone to check for responsiveness.

**Congratulations! Your AI-Stylist application is fully deployed and live on the internet.**

---

## Troubleshooting

-   **500 Internal Server Error on Frontend**: Check the Vercel logs. This usually means an environment variable is missing or incorrect.
-   **Backend Errors (502 Bad Gateway)**: Check the Render logs. This often points to a missing dependency in `requirements.txt` or an incorrect Start Command.
-   **CORS Errors in Browser Console**: Ensure your Vercel URL is correctly added to the `origins` list in your backend code and that the backend has been redeployed.
-   **"Failed to fetch" Errors**: Double-check that `NEXT_PUBLIC_API_URL` on Vercel points to your live Render backend URL, not `localhost`localhost.
