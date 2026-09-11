/* =====================================================================
   SZ VENTURES — Secure Auth & RBAC Logic
   Handles Supabase authentication, session state, and Role-Based Access.
   ===================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const forgotPasswordForm = document.getElementById('forgotPasswordForm');
  const logoutBtn = document.getElementById('logoutBtn');

  // Utility to show messages
  const showMessage = (msgId, text, isError = false) => {
    const el = document.getElementById(msgId);
    if (!el) return;
    el.textContent = text;
    el.style.color = isError ? '#ff4d4d' : '#4dff88';
    el.style.display = 'block';
  };

  // Ensure Supabase is loaded
  const requireSupabase = () => {
    if (!window.supabaseClient) {
      throw new Error("Supabase client is not configured. Please build with proper environment variables.");
    }
  };

  // Handle Login
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      const btn = loginForm.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.innerHTML = 'Signing in...';
      btn.disabled = true;

      try {
        requireSupabase();
        const { error } = await window.supabaseClient.auth.signInWithPassword({ email, password });
        if (error) throw error;
        window.location.href = '/portal/index.html';
      } catch (err) {
        showMessage('loginMessage', err.message, true);
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  }

  // Handle Register
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      const btn = registerForm.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.innerHTML = 'Registering...';
      btn.disabled = true;

      try {
        requireSupabase();
        const { error } = await window.supabaseClient.auth.signUp({ email, password });
        if (error) throw error;
        window.location.href = '/verify-email/index.html';
      } catch (err) {
        showMessage('registerMessage', err.message, true);
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  }

  // Handle Forgot Password
  if (forgotPasswordForm) {
    forgotPasswordForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const btn = forgotPasswordForm.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.innerHTML = 'Sending...';
      btn.disabled = true;

      try {
        requireSupabase();
        const { error } = await window.supabaseClient.auth.resetPasswordForEmail(email, {
          redirectTo: window.location.origin + '/portal/index.html',
        });
        if (error) throw error;
        showMessage('resetMessage', 'Check your email for the reset link.', false);
      } catch (err) {
        showMessage('resetMessage', err.message, true);
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  }

  // Handle Logout
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        requireSupabase();
        await window.supabaseClient.auth.signOut();
        window.location.href = '/login/index.html';
      } catch (err) {
        console.error("Logout failed", err);
      }
    });
  }

  // Handle Google Auth
  const googleBtn = document.getElementById('googleAuthBtn');
  if (googleBtn) {
    googleBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        requireSupabase();
        await window.supabaseClient.auth.signInWithOAuth({ provider: 'google' });
      } catch (err) {
        alert(err.message);
      }
    });
  }

  // Session check and RBAC on portal
  const isPortalRoute = window.location.pathname.includes('/portal');
  if (isPortalRoute) {
    const applyRBAC = (role) => {
      console.log("Applying RBAC for role:", role);
      // Elements that are restricted to ADMIN and PARTNER
      const adminElements = document.querySelectorAll('.restricted-admin');
      if (role !== 'ADMIN' && role !== 'PARTNER') {
        adminElements.forEach(el => el.style.display = 'none');
      }
      
      // Elements restricted to TEAM_MEMBER, ADMIN, PARTNER
      const teamElements = document.querySelectorAll('.restricted-team');
      if (role === 'CANDIDATE' || role === 'INVESTOR') {
        teamElements.forEach(el => el.style.display = 'none');
      }
      
      const roleDisplay = document.getElementById('userRoleDisplay');
      if(roleDisplay) roleDisplay.textContent = role;
    };

    const checkSession = async () => {
      try {
        requireSupabase();
        const { data: { session }, error } = await window.supabaseClient.auth.getSession();
        
        if (error || !session) {
          window.location.href = '/login/index.html';
          return;
        }

        // Display user email
        const emailEl = document.getElementById('userEmail');
        const avatarEl = document.querySelector('.avatar');
        if (emailEl) emailEl.textContent = session.user.email;
        if (avatarEl) avatarEl.textContent = session.user.email.charAt(0).toUpperCase();

        // Fetch Role from Profiles
        const { data: profile, error: profileError } = await window.supabaseClient
          .from('profiles')
          .select('role')
          .eq('id', session.user.id)
          .single();

        let userRole = 'CANDIDATE'; // Default fail-safe
        if (profile && !profileError) {
          userRole = profile.role;
        } else {
          console.error("Could not fetch profile role, defaulting to CANDIDATE.", profileError);
        }

        applyRBAC(userRole);

      } catch (err) {
        console.error("Session check failed", err);
        // If supabase fails to initialize, send to login to be safe
        window.location.href = '/login/index.html';
      }
    };
    checkSession();
  }
});
