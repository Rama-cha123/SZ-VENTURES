/* =====================================================================
   SZ VENTURES — Supabase Configuration
   DO NOT COMMIT REAL SECRETS IF REPOSITORY IS PUBLIC
   ===================================================================== */

const SUPABASE_URL = 'https://rrggifbazlirccotjsfb.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJyZ2dpZmJhemxpcmNjb3Rqc2ZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk2Mzg2NDcsImV4cCI6MjEwNTIxNDY0N30.VKjCu7UbYGsRO6ZKMyik_ufvu2X3VkbWKYsz_U3IcTg';

if (SUPABASE_URL.startsWith('%')) {
  console.warn('Supabase URL and Anon Key are not set. Auth features will fail.');
}

window.supabaseClient = null;

if (typeof window.supabase !== 'undefined' && !SUPABASE_URL.startsWith('%')) {
  window.supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    flowType: 'pkce',
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
});
}

