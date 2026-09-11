/* =====================================================================
   SZX VENTURES — Supabase Configuration
   DO NOT COMMIT REAL SECRETS IF REPOSITORY IS PUBLIC
   ===================================================================== */

const SUPABASE_URL = '%SUPABASE_URL%';
const SUPABASE_ANON_KEY = '%SUPABASE_ANON_KEY%';

if (SUPABASE_URL === '%SUPABASE_URL%') {
  console.warn('Supabase URL and Anon Key are not set. Auth features will fail.');
}

window.supabaseClient = null;

if (typeof window.supabase !== 'undefined' && SUPABASE_URL !== '%SUPABASE_URL%') {
  window.supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
}
