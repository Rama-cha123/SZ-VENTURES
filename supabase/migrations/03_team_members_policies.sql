-- 03_team_members_policies.sql
-- Add missing RLS policies for team_members table
-- Without these, nobody (including admins) can read or manage team memberships through the portal.

-- Admins can view all team memberships
CREATE POLICY "Admins can view all team members" ON public.team_members
  FOR SELECT USING (public.is_admin());

-- Members can view team members of their own ventures
CREATE POLICY "Members can view venture team members" ON public.team_members
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.team_members AS tm
      WHERE tm.user_id = auth.uid() AND tm.venture_id = public.team_members.venture_id
    )
  );

-- Admins can manage all team memberships
CREATE POLICY "Admins manage team members" ON public.team_members
  FOR ALL USING (public.is_admin());
