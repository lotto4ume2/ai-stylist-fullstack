-- Enhanced AI-Stylist Database Schema
-- Execute this in Supabase SQL Editor after the base schema

-- Add new columns to clothing_items table for enhanced features
ALTER TABLE public.clothing_items 
ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS tags TEXT[],
ADD COLUMN IF NOT EXISTS season TEXT,
ADD COLUMN IF NOT EXISTS times_worn INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_worn_date TIMESTAMP WITH TIME ZONE;

-- Create outfit_history table
CREATE TABLE IF NOT EXISTS public.outfit_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    outfit_name TEXT,
    item_ids UUID[] NOT NULL,
    worn_date DATE NOT NULL,
    occasion TEXT,
    weather TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create favorites table for quick access
CREATE TABLE IF NOT EXISTS public.favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    item_id UUID NOT NULL REFERENCES public.clothing_items(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, item_id)
);

-- Create outfit_plans table
CREATE TABLE IF NOT EXISTS public.outfit_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    outfit_name TEXT NOT NULL,
    item_ids UUID[] NOT NULL,
    planned_date DATE,
    occasion TEXT,
    notes TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create shared_outfits table for social features
CREATE TABLE IF NOT EXISTS public.shared_outfits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    outfit_name TEXT NOT NULL,
    item_ids UUID[] NOT NULL,
    description TEXT,
    share_token TEXT UNIQUE NOT NULL,
    view_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_outfit_history_user_id ON public.outfit_history(user_id);
CREATE INDEX IF NOT EXISTS idx_outfit_history_worn_date ON public.outfit_history(worn_date DESC);
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON public.favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_outfit_plans_user_id ON public.outfit_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_outfit_plans_planned_date ON public.outfit_plans(planned_date);
CREATE INDEX IF NOT EXISTS idx_shared_outfits_share_token ON public.shared_outfits(share_token);
CREATE INDEX IF NOT EXISTS idx_clothing_items_favorite ON public.clothing_items(user_id, is_favorite);
CREATE INDEX IF NOT EXISTS idx_clothing_items_tags ON public.clothing_items USING GIN(tags);

-- Enable Row Level Security
ALTER TABLE public.outfit_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.outfit_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.shared_outfits ENABLE ROW LEVEL SECURITY;

-- RLS Policies for outfit_history
CREATE POLICY "Users can view their own outfit history"
    ON public.outfit_history FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own outfit history"
    ON public.outfit_history FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own outfit history"
    ON public.outfit_history FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own outfit history"
    ON public.outfit_history FOR DELETE
    USING (auth.uid() = user_id);

-- RLS Policies for favorites
CREATE POLICY "Users can view their own favorites"
    ON public.favorites FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can add favorites"
    ON public.favorites FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove favorites"
    ON public.favorites FOR DELETE
    USING (auth.uid() = user_id);

-- RLS Policies for outfit_plans
CREATE POLICY "Users can view their own outfit plans"
    ON public.outfit_plans FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create outfit plans"
    ON public.outfit_plans FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their outfit plans"
    ON public.outfit_plans FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their outfit plans"
    ON public.outfit_plans FOR DELETE
    USING (auth.uid() = user_id);

-- RLS Policies for shared_outfits
CREATE POLICY "Users can view their own shared outfits"
    ON public.shared_outfits FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Public can view shared outfits by token"
    ON public.shared_outfits FOR SELECT
    USING (is_public = TRUE);

CREATE POLICY "Users can create shared outfits"
    ON public.shared_outfits FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their shared outfits"
    ON public.shared_outfits FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their shared outfits"
    ON public.shared_outfits FOR DELETE
    USING (auth.uid() = user_id);

-- Create trigger for outfit_plans updated_at
CREATE TRIGGER update_outfit_plans_updated_at
    BEFORE UPDATE ON public.outfit_plans
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create function to increment view count
CREATE OR REPLACE FUNCTION increment_outfit_view_count(outfit_share_token TEXT)
RETURNS void AS $$
BEGIN
    UPDATE public.shared_outfits
    SET view_count = view_count + 1
    WHERE share_token = outfit_share_token;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
