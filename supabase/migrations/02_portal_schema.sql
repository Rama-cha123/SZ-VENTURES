-- 02_portal_schema.sql
-- Strict RBAC Schema for SZ Ventures Portal

-- 1. Ventures
CREATE TABLE IF NOT EXISTS public.ventures (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',
    owner_id UUID REFERENCES auth.users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Team Members (Explicit Memberships)
CREATE TABLE IF NOT EXISTS public.team_members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    venture_id UUID REFERENCES public.ventures(id) ON DELETE RESTRICT,
    user_id UUID REFERENCES auth.users(id) ON DELETE RESTRICT,
    role TEXT NOT NULL DEFAULT 'TEAM_MEMBER',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(venture_id, user_id)
);

-- 3. Projects
CREATE TABLE IF NOT EXISTS public.projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    venture_id UUID REFERENCES public.ventures(id) ON DELETE RESTRICT,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'planning',
    assigned_to UUID REFERENCES auth.users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Documents
CREATE TABLE IF NOT EXISTS public.documents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    venture_id UUID REFERENCES public.ventures(id) ON DELETE RESTRICT,
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    uploader_id UUID REFERENCES auth.users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS
ALTER TABLE public.ventures ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;

-- Helper function to check if user is global admin
CREATE OR REPLACE FUNCTION public.is_admin() RETURNS BOOLEAN AS $$
  SELECT EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'ADMIN');
$$ LANGUAGE sql SECURITY DEFINER;

-- VENTURES POLICIES
-- Select: Admins see all, others see only where they are members
CREATE POLICY "Admins can view all ventures" ON public.ventures FOR SELECT USING (public.is_admin());
CREATE POLICY "Members can view explicit ventures" ON public.ventures FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.ventures.id)
);
-- Insert/Update: Admins only
CREATE POLICY "Admins manage ventures" ON public.ventures FOR ALL USING (public.is_admin());

-- PROJECTS POLICIES
-- Select: Admins see all, others see projects of their ventures
CREATE POLICY "Admins can view all projects" ON public.projects FOR SELECT USING (public.is_admin());
CREATE POLICY "Members can view venture projects" ON public.projects FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.projects.venture_id)
);
-- Insert/Update: Admins OR Partners/Members of the specific venture
CREATE POLICY "Admins manage projects" ON public.projects FOR ALL USING (public.is_admin());
CREATE POLICY "Venture members can manage projects" ON public.projects FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.projects.venture_id AND role IN ('PARTNER', 'TEAM_MEMBER'))
);
CREATE POLICY "Venture members can update projects" ON public.projects FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.projects.venture_id AND role IN ('PARTNER', 'TEAM_MEMBER'))
);

-- DOCUMENTS POLICIES
CREATE POLICY "Admins can view all documents metadata" ON public.documents FOR SELECT USING (public.is_admin());
CREATE POLICY "Members can view venture documents metadata" ON public.documents FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.documents.venture_id)
);
CREATE POLICY "Admins manage documents metadata" ON public.documents FOR ALL USING (public.is_admin());
CREATE POLICY "Venture members can insert documents metadata" ON public.documents FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.documents.venture_id AND role IN ('PARTNER', 'TEAM_MEMBER'))
);
CREATE POLICY "Venture members can update documents metadata" ON public.documents FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.team_members WHERE user_id = auth.uid() AND venture_id = public.documents.venture_id AND role IN ('PARTNER', 'TEAM_MEMBER'))
);
