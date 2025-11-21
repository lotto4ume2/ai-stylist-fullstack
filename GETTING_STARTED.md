# Getting Started with AI-Stylist

This guide will walk you through setting up the AI-Stylist application from scratch. Perfect for beginners!

## What You'll Build

A full-stack digital closet application where users can:
- Create an account and login
- Upload photos of their clothing
- Organize items with categories, colors, and brands
- View all items in a beautiful grid layout
- Delete items they no longer want

## Prerequisites

Before you begin, make sure you have:

- **Computer**: Mac, Windows, or Linux
- **Internet connection**: For downloading packages and accessing Supabase
- **Text editor**: VS Code (recommended), Sublime Text, or any code editor
- **Terminal/Command Prompt**: For running commands

## Step 1: Install Required Software

### 1.1 Install Node.js

Node.js is required for the frontend.

1. Go to https://nodejs.org
2. Download the **LTS version** (20.x or higher)
3. Run the installer
4. Verify installation:
   ```bash
   node --version
   # Should show v20.x.x or higher
   ```

### 1.2 Install pnpm

pnpm is a fast package manager for Node.js.

```bash
npm install -g pnpm
```

Verify:
```bash
pnpm --version
```

### 1.3 Install Python

Python is required for the backend.

1. Go to https://python.org
2. Download **Python 3.11** or higher
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python3 --version
   # Should show Python 3.11.x or higher
   ```

### 1.4 Install pip

pip usually comes with Python. Verify:

```bash
pip3 --version
```

### 1.5 Install Git (Optional but Recommended)

1. Go to https://git-scm.com
2. Download and install
3. Verify:
   ```bash
   git --version
   ```

## Step 2: Set Up Supabase

Supabase provides authentication, database, and file storage.

### 2.1 Create Supabase Account

1. Go to https://supabase.com
2. Click **"Start your project"**
3. Sign up with GitHub, Google, or email
4. Verify your email

### 2.2 Create a New Project

1. Click **"New project"**
2. Fill in:
   - **Organization**: Create new or select existing
   - **Name**: `ai-stylist` (or any name you like)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to you
3. Click **"Create new project"**
4. Wait 1-2 minutes for setup

### 2.3 Get API Credentials

1. In your project dashboard, go to **Settings** (gear icon)
2. Click **API** in the sidebar
3. You'll see:
   - **Project URL**: Copy this (e.g., `https://xxxxx.supabase.co`)
   - **anon public key**: Copy this
   - **service_role key**: Copy this (keep it secret!)

**Save these values** - you'll need them soon!

### 2.4 Set Up Database

1. Go to **SQL Editor** in the left sidebar
2. Click **"New query"**
3. Open the file `backend/schema.sql` from the project
4. Copy all the SQL code
5. Paste it into the SQL Editor
6. Click **"Run"**
7. You should see "Success. No rows returned"

### 2.5 Create Storage Bucket

1. Go to **Storage** in the left sidebar
2. Click **"Create a new bucket"**
3. Fill in:
   - **Name**: `clothing-items`
   - **Public bucket**: ✓ Check this
   - **File size limit**: 5 MB
4. Click **"Create bucket"**

### 2.6 Set Up Storage Policies

1. Click on the `clothing-items` bucket
2. Go to **Policies** tab
3. Click **"New policy"**
4. Select **"For full customization"**

**Policy 1: Upload**
- **Policy name**: Authenticated users can upload
- **Allowed operation**: INSERT
- **Target roles**: authenticated
- **WITH CHECK**: `bucket_id = 'clothing-items'`
- Click **"Review"** then **"Save policy"**

**Policy 2: Read**
- **Policy name**: Public read access
- **Allowed operation**: SELECT
- **Target roles**: public
- **USING**: `bucket_id = 'clothing-items'`
- Click **"Review"** then **"Save policy"**

**Policy 3: Delete**
- **Policy name**: Users can delete their own
- **Allowed operation**: DELETE
- **Target roles**: authenticated
- **USING**: `bucket_id = 'clothing-items' AND (storage.foldername(name))[1] = auth.uid()::text`
- Click **"Review"** then **"Save policy"**

### 2.7 Disable Email Confirmation (For Development)

1. Go to **Authentication** → **Settings**
2. Scroll to **Email Auth**
3. **Disable** "Enable email confirmations"
4. Click **"Save"**

This allows you to test without email verification.

## Step 3: Set Up the Backend

### 3.1 Download the Project

If you have Git:
```bash
git clone https://github.com/yourusername/ai-stylist.git
cd ai-stylist
```

Or download the ZIP file and extract it.

### 3.2 Navigate to Backend

```bash
cd backend
```

### 3.3 Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

This will install FastAPI, Supabase client, and other dependencies.

### 3.4 Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

Now edit `.env` with your text editor and fill in:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key
SECRET_KEY=generate-this-next
ENVIRONMENT=development
```

### 3.5 Generate SECRET_KEY

Run this command:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste it as your `SECRET_KEY` in `.env`.

### 3.6 Start the Backend Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend is now running.

### 3.7 Test the Backend

Open a new terminal and run:

```bash
curl http://localhost:8000/
```

You should see:
```json
{
  "message": "AI-Stylist API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

Or open http://localhost:8000/docs in your browser to see the API documentation.

## Step 4: Set Up the Frontend

### 4.1 Open New Terminal

Keep the backend running and open a **new terminal window**.

### 4.2 Navigate to Frontend

```bash
cd frontend
# If you're in the backend directory:
cd ../frontend
```

### 4.3 Install Dependencies

```bash
pnpm install
```

This will take 1-2 minutes to download all packages.

### 4.4 Create Environment File

```bash
cp .env.local.example .env.local
```

The default content should be:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This is correct for local development!

### 4.5 Start the Frontend Server

```bash
pnpm dev
```

You should see:
```
▲ Next.js 16.0.3
- Local:        http://localhost:3000
✓ Ready in 2.5s
```

## Step 5: Test the Application

### 5.1 Open the App

Open your browser and go to:
```
http://localhost:3000
```

You should see the AI-Stylist landing page!

### 5.2 Create an Account

1. Click **"Sign Up"**
2. Fill in:
   - **Full Name**: Your name (optional)
   - **Email**: Your email
   - **Password**: At least 8 characters
   - **Confirm Password**: Same password
3. Click **"Sign Up"**

You should be redirected to your closet!

### 5.3 Upload Your First Item

1. Click **"Add Item"** or **"Upload Your First Item"**
2. Click the upload area to select an image
3. Choose a photo of clothing from your computer
4. Fill in (all optional):
   - **Category**: Select from dropdown
   - **Color**: e.g., "Blue"
   - **Brand**: e.g., "Nike"
   - **Notes**: Any notes about the item
5. Click **"Upload Item"**

You should see a success message and be redirected to your closet!

### 5.4 View Your Closet

Your uploaded item should now appear in a grid view with:
- The image
- Category badge
- Brand and color
- Notes
- Upload date
- Delete button

### 5.5 Test Logout and Login

1. Click **"Logout"** in the top right
2. You'll be redirected to the home page
3. Click **"Login"**
4. Enter your email and password
5. You should see your closet with your items!

## Step 6: Verify Everything Works

### Checklist

✓ Backend running on http://localhost:8000
✓ Frontend running on http://localhost:3000
✓ Can create an account
✓ Can login
✓ Can upload images
✓ Images appear in closet
✓ Can delete items
✓ Can logout

## Common Issues and Solutions

### Issue: "Port 8000 is already in use"

**Solution**: Another program is using port 8000. Either:
- Stop the other program
- Or use a different port:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8001
  ```
  Then update frontend `.env.local` to `http://localhost:8001`

### Issue: "Module not found" (Backend)

**Solution**: Make sure you're in the backend directory and run:
```bash
pip3 install -r requirements.txt
```

### Issue: "Module not found" (Frontend)

**Solution**: Make sure you're in the frontend directory and run:
```bash
pnpm install
```

### Issue: "Could not validate credentials"

**Solution**: Check that:
- Backend `.env` has correct Supabase credentials
- Frontend `.env.local` has correct backend URL
- Both servers are running

### Issue: "Upload failed"

**Solution**: Check that:
- Supabase storage bucket `clothing-items` exists
- Storage policies are set up correctly
- Image is less than 5MB
- Image is a valid format (JPG, PNG, WEBP)

### Issue: Can't see uploaded images

**Solution**: Check:
- Supabase storage bucket is **public**
- Storage policies allow public read access
- Check browser console for errors (F12)

## Next Steps

Now that everything is working locally, you can:

1. **Add more items** to your closet
2. **Customize the UI** - Edit the Tailwind classes
3. **Deploy to production** - See `DEPLOYMENT.md` files
4. **Add new features** - Check the roadmap in main README
5. **Learn the code** - Explore the files and understand how it works

## Learning Resources

### Backend (FastAPI)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Python for Beginners](https://www.python.org/about/gettingstarted/)

### Frontend (Next.js)
- [Next.js Tutorial](https://nextjs.org/learn)
- [React Documentation](https://react.dev/learn)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

### Database (Supabase)
- [Supabase Documentation](https://supabase.com/docs)
- [SQL Tutorial](https://www.w3schools.com/sql/)

### Styling (Tailwind CSS)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## Getting Help

If you're stuck:

1. **Check the error message** - It usually tells you what's wrong
2. **Check the documentation** - README files in each directory
3. **Check browser console** - Press F12 in your browser
4. **Check server logs** - Look at the terminal where servers are running
5. **Search online** - Copy the error message and search
6. **Ask for help** - Open an issue on GitHub

## Tips for Success

1. **Keep both servers running** - Backend and frontend need to run simultaneously
2. **Check the browser console** - Press F12 to see errors
3. **Read error messages carefully** - They usually tell you exactly what's wrong
4. **Test one thing at a time** - Don't make multiple changes before testing
5. **Save your work** - Use Git to commit changes regularly
6. **Don't be afraid to experiment** - You can always start over!

## Congratulations! 🎉

You've successfully set up a full-stack web application with:
- User authentication
- Database storage
- File uploads
- Modern UI
- RESTful API

This is a significant achievement! You now have a solid foundation to build upon.

Happy coding! 🚀
