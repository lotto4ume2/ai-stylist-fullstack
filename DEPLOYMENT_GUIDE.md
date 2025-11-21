# AI-Stylist: Complete Deployment Guide

**Author**: Manus AI  
**Date**: November 21, 2025  
**Status**: ✅ Ready for Production Deployment

---

## Introduction

This guide provides comprehensive instructions for deploying the AI Stylist full-stack application to various hosting platforms. The project is ready for deployment with all necessary configuration files included.

**By the end of this guide, you will have a live, publicly accessible web application.**

### Prerequisites

Before you begin, ensure you have the following:

1.  **GitHub Account**: Your project code should be in a GitHub repository.
2.  **Render Account**: Sign up for free at [render.com](https://render.com).
3.  **Vercel Account**: Sign up for free at [vercel.com](https://vercel.com).
4.  **Node.js & pnpm**: Installed on your local machine for final checks.
5.  **Vercel CLI**: Install globally by running `npm install -g vercel`.

---

## Backend Deployment (Choose One)



### Option 1: Deploy to Render

Render is a user-friendly platform that simplifies deployment. We have already configured the `render.yaml` file for you.







1. **Create a Render Account**: Sign up at [render.com](https://render.com) using your GitHub account.
2. **Create a New Blueprint Service**:
   - In the Render dashboard, click **New > Blueprint**.
   - Select your `ai-stylist-fullstack` repository.
   - Render will automatically detect and use the `render.yaml` file.





3. **Add Environment Variables**:

   - Render will prompt you to add the secret environment variables. Copy and paste the following values from your `backend/.env` file:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `SUPABASE_SERVICE_KEY`
     - `SECRET_KEY`

4. **Deploy**:

Click **"Create New Blueprint Service"**. Render will build and deploy your backend.





---

### Option 2: Deploy to Fly.io

Fly.io is a flexible platform that deploys applications in Docker containers.

1. **Install `flyctl`**: Follow the instructions at [fly.io/install.sh](https://fly.io/install.sh) to install the command-line tool.
2. **Sign Up and Log In**:
   - Run `fly auth signup` to create an account.
   - Run `fly auth login` to log in.
3. **Launch the App**:
   - Navigate to the `backend` directory: `cd backend`
   - Run `fly launch`. Fly.io will detect the `fly.toml` file and configure the deployment.
   - **Do not** set up a Postgres database when prompted.
4. **Set Secrets**:
   - Run the following commands to set your environment variables:
     ```bash
     fly secrets set SUPABASE_URL="your_supabase_url"
     fly secrets set SUPABASE_KEY="your_supabase_key"
     fly secrets set SUPABASE_SERVICE_KEY="your_supabase_service_key"
     fly secrets set SECRET_KEY="your_secret_key"
     fly secrets set ENVIRONMENT="production"
     ```
5. **Deploy**:
   - Run `fly deploy` to build and deploy your backend.

### Option 3: Deploy to Railway

Railway offers a simple deployment experience with a focus on developer productivity.

1. **Create a Railway Account**: Sign up at [railway.app](https://railway.app) with your GitHub account.
2. **Create a New Project**:
   - In the Railway dashboard, click **New Project**.
   - Select **Deploy from GitHub repo** and choose your `ai-stylist-fullstack` repository.
3. **Configure Service**:
   - Railway will automatically detect the `railway.json` file and configure the service.
4. **Add Environment Variables**:
   - In the service settings, go to the **Variables** tab.
   - Add the following variables from your `backend/.env` file:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `SUPABASE_SERVICE_KEY`
     - `SECRET_KEY`
     - `ENVIRONMENT` (set to `production`)
5. **Deploy**: Railway will automatically build and deploy your backend.

## Frontend Deployment (Vercel)

Vercel is the recommended platform for deploying Next.js applications.





1. **Create a Vercel Account**: Sign up at [vercel.com](https://vercel.com) with your GitHub account.
2. **Create a New Project**:
   - In the Vercel dashboard, click **Add New... > Project**.
   - Select your `ai-stylist-fullstack` repository.

3. **Configure Project**:

   - Vercel will automatically detect the Next.js framework.
   - Set the **Root Directory** to `frontend`.

4. **Add Environment Variables**:

   - In the project settings, go to **Environment Variables**.
   - Add the following variable:
     - `NEXT_PUBLIC_BACKEND_URL`: The URL of your deployed backend (from Render, Fly.io, or Railway).

5. **Deploy**:

Click **Deploy**. Vercel will build and deploy your frontend.

---

## Post-Deployment: CORS Configuration

After deploying your frontend, you need to add its URL to your Supabase CORS configuration to allow requests.

1. **Get Frontend URL**: Copy the production URL of your frontend from the Vercel dashboard.
2. **Update Supabase CORS Settings**:
   - Go to your Supabase project dashboard.
   - Navigate to **Authentication > URL Configuration**.
   - In the **Redirect URLs** section, add your frontend URL.

Your AI Stylist application is now fully deployed and ready to use!

---


