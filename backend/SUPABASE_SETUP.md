# Supabase Setup Guide for AI-Stylist

This guide will walk you through setting up Supabase for the AI-Stylist application, including authentication, database tables, and storage buckets.

## Step 1: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign up or log in
2. Click **"New Project"**
3. Fill in the project details:
   - **Name**: AI-Stylist (or your preferred name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose the region closest to your users
4. Click **"Create new project"** and wait for setup to complete (1-2 minutes)

## Step 2: Get Your API Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. You'll need these values for your `.env` file:
   - **Project URL**: Copy the URL (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key**: Copy the `anon` `public` key
   - **service_role key**: Copy the `service_role` `secret` key (keep this secure!)

3. Update your backend `.env` file:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-public-key
   SUPABASE_SERVICE_KEY=your-service-role-key
   SECRET_KEY=your-generated-secret-key
   ```

## Step 3: Enable Email Authentication

1. Go to **Authentication** → **Providers** in your Supabase dashboard
2. Ensure **Email** is enabled (it should be by default)
3. Configure email settings:
   - **Enable email confirmations**: You can disable this for development
   - For production, configure your email provider (SendGrid, AWS SES, etc.)

### Development Mode (Disable Email Confirmation)

For easier development, you can disable email confirmation:

1. Go to **Authentication** → **Settings**
2. Scroll to **Email Auth**
3. **Disable** "Enable email confirmations"
4. Click **Save**

This allows users to sign up and log in immediately without email verification.

## Step 4: Create Database Tables

1. Go to **SQL Editor** in your Supabase dashboard
2. Click **"New query"**
3. Copy and paste the following SQL schema:

```sql
-- Create clothing_items table
CREATE TABLE IF NOT EXISTS public.clothing_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    category TEXT,
    color TEXT,
    brand TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_clothing_items_user_id ON public.clothing_items(user_id);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_clothing_items_created_at ON public.clothing_items(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE public.clothing_items ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only view their own items
CREATE POLICY "Users can view their own clothing items"
    ON public.clothing_items
    FOR SELECT
    USING (auth.uid() = user_id);

-- Create policy: Users can insert their own items
CREATE POLICY "Users can insert their own clothing items"
    ON public.clothing_items
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Create policy: Users can update their own items
CREATE POLICY "Users can update their own clothing items"
    ON public.clothing_items
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Create policy: Users can delete their own items
CREATE POLICY "Users can delete their own clothing items"
    ON public.clothing_items
    FOR DELETE
    USING (auth.uid() = user_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_clothing_items_updated_at
    BEFORE UPDATE ON public.clothing_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

4. Click **"Run"** to execute the SQL
5. You should see a success message

## Step 5: Create Storage Bucket

1. Go to **Storage** in your Supabase dashboard
2. Click **"Create a new bucket"**
3. Configure the bucket:
   - **Name**: `clothing-items`
   - **Public bucket**: ✓ Check this box (we need public URLs for images)
   - **File size limit**: 5 MB (adjust as needed)
   - **Allowed MIME types**: `image/jpeg`, `image/png`, `image/jpg`, `image/webp`
4. Click **"Create bucket"**

## Step 6: Configure Storage Policies

By default, the bucket needs security policies. Let's set them up:

1. Click on the `clothing-items` bucket
2. Go to **Policies** tab
3. Click **"New policy"**

### Policy 1: Allow authenticated users to upload

```sql
CREATE POLICY "Authenticated users can upload images"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'clothing-items');
```

### Policy 2: Allow public read access

```sql
CREATE POLICY "Public read access for clothing items"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'clothing-items');
```

### Policy 3: Allow users to delete their own files

```sql
CREATE POLICY "Users can delete their own images"
ON storage.objects FOR DELETE
TO authenticated
USING (
    bucket_id = 'clothing-items' 
    AND (storage.foldername(name))[1] = auth.uid()::text
);
```

Alternatively, you can use the Supabase UI to create these policies:

1. Click **"New policy"**
2. Choose **"For full customization"**
3. Fill in:
   - **Policy name**: "Authenticated users can upload"
   - **Allowed operation**: INSERT
   - **Target roles**: authenticated
   - **WITH CHECK expression**: `bucket_id = 'clothing-items'`
4. Repeat for the other policies

## Step 7: Verify Setup

### Test Database Connection

1. Go to **Table Editor** in Supabase
2. You should see the `clothing_items` table
3. Click on it to view the structure

### Test Storage Bucket

1. Go to **Storage** → `clothing-items`
2. Try uploading a test image manually
3. Verify you can see the public URL

## Step 8: Update CORS Settings (If Needed)

Supabase automatically handles CORS for authenticated requests, but if you encounter issues:

1. Go to **Settings** → **API**
2. Check **CORS settings**
3. Add your frontend URLs if needed (usually not required)

## Database Schema Explanation

### clothing_items Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier (auto-generated) |
| `user_id` | UUID | Foreign key to auth.users (who owns this item) |
| `image_url` | TEXT | Public URL of the uploaded image |
| `category` | TEXT | Clothing category (e.g., "shirt", "pants") |
| `color` | TEXT | Primary color of the item |
| `brand` | TEXT | Brand name |
| `notes` | TEXT | User notes about the item |
| `created_at` | TIMESTAMP | When the item was added |
| `updated_at` | TIMESTAMP | Last update time (auto-updated) |

### Row Level Security (RLS)

RLS ensures that:
- Users can only see their own clothing items
- Users can only modify their own items
- Database-level security (even if API is compromised)

### Storage Structure

Files are organized by user ID:
```
clothing-items/
  ├── user-id-1/
  │   ├── uuid-1.jpg
  │   └── uuid-2.png
  └── user-id-2/
      └── uuid-3.jpg
```

## Troubleshooting

### Issue: "JWT expired" errors

**Solution**: Check that your `SECRET_KEY` in the backend matches and hasn't changed.

### Issue: "Permission denied" when uploading

**Solution**: Verify storage policies are correctly set and bucket is public.

### Issue: Can't insert into clothing_items table

**Solution**: Check that RLS policies are created and user is authenticated.

### Issue: Email confirmation required

**Solution**: Disable email confirmation in Authentication → Settings for development.

## Next Steps

1. Test the backend API with your Supabase credentials
2. Create a test user via the signup endpoint
3. Try uploading an image
4. Verify data appears in Supabase dashboard

## Security Best Practices

✓ **Never commit** `.env` file with real credentials
✓ **Use service_role key** only on the backend (never expose to frontend)
✓ **Enable RLS** on all tables with user data
✓ **Use HTTPS** in production
✓ **Enable email confirmation** in production
✓ **Set up proper backup** policies for your database
✓ **Monitor usage** in Supabase dashboard to stay within free tier limits

## Supabase Free Tier Limits

- **Database**: 500 MB
- **Storage**: 1 GB
- **Bandwidth**: 2 GB/month
- **Monthly Active Users**: Unlimited

For production, consider upgrading to Pro tier for better limits and support.
