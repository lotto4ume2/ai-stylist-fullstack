-- AI-Stylist Database Schema
-- Execute this in Supabase SQL Editor

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

-- Storage policies (run these in Storage → Policies section)
-- Note: These need to be created through the Supabase UI or using the storage schema

-- Policy 1: Allow authenticated users to upload
-- CREATE POLICY "Authenticated users can upload images"
-- ON storage.objects FOR INSERT
-- TO authenticated
-- WITH CHECK (bucket_id = 'clothing-items');

-- Policy 2: Allow public read access
-- CREATE POLICY "Public read access for clothing items"
-- ON storage.objects FOR SELECT
-- TO public
-- USING (bucket_id = 'clothing-items');

-- Policy 3: Allow users to delete their own files
-- CREATE POLICY "Users can delete their own images"
-- ON storage.objects FOR DELETE
-- TO authenticated
-- USING (
--     bucket_id = 'clothing-items' 
--     AND (storage.foldername(name))[1] = auth.uid()::text
-- );
