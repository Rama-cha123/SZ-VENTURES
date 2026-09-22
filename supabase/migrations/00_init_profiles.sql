-- Migration: Create Profiles Table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  role TEXT DEFAULT 'CANDIDATE' CHECK (role IN ('ADMIN', 'PARTNER', 'TEAM_MEMBER', 'INVESTOR', 'CANDIDATE')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can ONLY read their own profile. They cannot read others.
CREATE POLICY "Users can read own profile" ON profiles 
  FOR SELECT USING (auth.uid() = id);

-- No UPDATE policy exists here for standard users.
-- This ensures users cannot modify their own privileged role to gain access.
-- Admins must update this manually in the database or via a privileged Edge Function.
