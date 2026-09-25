// portal.js
// Handles frontend routing and data fetching for the SZ Ventures Portal

document.addEventListener('DOMContentLoaded', () => {
    const isPortalRoute = window.location.pathname.includes('/portal');
    if (!isPortalRoute) return;

    const mainContent = document.querySelector('.dashboard');
    if (!mainContent) return;

    // --- Core Navigation Router ---
    const route = async () => {
        const hash = window.location.hash || '#dashboard';
        
        // Update sidebar active states
        document.querySelectorAll('.sidebar-nav .nav-item').forEach(el => {
            el.classList.remove('active');
            if(el.getAttribute('href') === hash) el.classList.add('active');
        });

        // Clear and show loading
        mainContent.innerHTML = `<div style="padding: 2rem; color: var(--muted);">Loading ${hash.replace('#','')}...</div>`;
        
        // Update topbar header
        const topbarHeader = document.querySelector('.topbar-left h2');
        if (topbarHeader) {
            let titleText = hash.replace('#', '');
            titleText = titleText.charAt(0).toUpperCase() + titleText.slice(1);
            if (titleText === 'Dashboard') titleText = 'Dashboard Overview';
            topbarHeader.textContent = titleText;
        }

        try {
            const { data: sessionData } = await window.supabaseClient.auth.getSession();
            if (!sessionData || !sessionData.session) return; // Auth.js will redirect

            if (hash === '#dashboard') await renderDashboard();
            else if (hash === '#overview') await renderOverview();
            else if (hash === '#ventures') await renderVentures();
            else if (hash === '#team') await renderTeam();
            else if (hash === '#projects') await renderProjects();
            else if (hash === '#documents') await renderDocuments();
            else if (hash === '#reports') await renderReports();
            else if (hash === '#settings') await renderSettings();
            else if (hash === '#access control') await renderSettings();
            else await renderDashboard();
        } catch (err) {
            handleError(err);
        }
    };

    window.addEventListener('hashchange', route);
    
    // --- Error & Empty State Handlers ---
    const handleError = (err) => {
        console.error("Portal Route Error:", err);
        mainContent.innerHTML = `
            <div class="panel" style="padding: 2rem; border-color: #ff4d4d; background: rgba(255, 77, 77, 0.05);">
                <h3 style="color: #ff4d4d; margin-top: 0;">Error Loading View</h3>
                <p>${err.message || 'An unexpected error occurred.'}</p>
                <p style="font-size: var(--fs-300); color: var(--muted);">${err.details || ''}</p>
            </div>
        `;
    };

    const emptyState = (message) => {
        return `
            <div class="panel" style="padding: 3rem 2rem; text-align: center;">
                <p style="color: var(--muted); font-size: var(--fs-400);">${message}</p>
            </div>
        `;
    };

    // --- View Renderers ---
    
    const renderDashboard = async () => {
        // Fetch permitted ventures
        const { data: ventures, error } = await window.supabaseClient.from('ventures').select('*');
        if (error) throw error;

        let venturesHtml = '';
        if (!ventures || ventures.length === 0) {
            venturesHtml = `<tr><td colspan="4" style="text-align:center;">No accessible ventures found.</td></tr>`;
        } else {
            venturesHtml = ventures.map(v => `
                <tr>
                    <td><strong>${v.name}</strong></td>
                    <td>${v.description || 'N/A'}</td>
                    <td><span class="status-dot ${v.status === 'active' ? 'status-active' : 'status-pending'}"></span>${v.status}</td>
                    <td><a href="#ventures" onclick="window.currentVentureId='${v.id}'" style="color:var(--gold);">View</a></td>
                </tr>
            `).join('');
        }

        mainContent.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-label">Accessible Ventures</span>
                    <div class="stat-value">${ventures ? ventures.length : 0}</div>
                    <div class="stat-diff"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg> Operational</div>
                </div>
            </div>
            <div class="panel">
                <div class="panel-header">
                    <h3 class="panel-title">Your Ventures</h3>
                    <a href="#ventures" style="color: var(--gold); text-decoration: none; font-size: var(--fs-400);">View all →</a>
                </div>
                <table class="data-table">
                    <thead><tr><th>Venture</th><th>Description</th><th>Status</th><th>Action</th></tr></thead>
                    <tbody>${venturesHtml}</tbody>
                </table>
            </div>
        `;
    };

    const renderVentures = async () => {
        const { data: ventures, error } = await window.supabaseClient.from('ventures').select('*');
        if (error) throw error;

        if (!ventures || ventures.length === 0) {
            mainContent.innerHTML = emptyState('You are not currently linked to any ventures.');
            return;
        }

        mainContent.innerHTML = `
            <h2>Ventures Directory</h2>
            <div class="stats-grid">
                ${ventures.map(v => `
                    <div class="stat-card">
                        <h3 style="margin-top:0;">${v.name}</h3>
                        <p style="font-size: var(--fs-400); color: var(--muted);">${v.description || ''}</p>
                        <div class="stat-diff"><span class="status-dot status-active"></span>${v.status}</div>
                    </div>
                `).join('')}
            </div>
        `;
    };

    const renderOverview = async () => {
        const { data: projects, error } = await window.supabaseClient.from('projects').select('id, status');
        if (error) throw error;
        
        const active = projects ? projects.filter(p => p.status !== 'archived').length : 0;
        
        mainContent.innerHTML = `
            <h2>Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-label">Total Active Projects</span>
                    <div class="stat-value">${active}</div>
                </div>
            </div>
        `;
    };

    const renderTeam = async () => {
        const { data: members, error } = await window.supabaseClient
            .from('team_members')
            .select('*, ventures(name)');
            
        if (error) throw error;

        let html = `<h2>Team Directory</h2>`;
        
        // Invite mock form
        html += `
            <div class="panel" style="padding: 1.5rem; margin-bottom: 2rem;">
                <h3 style="margin-top:0;">Invite Team Member (Mock)</h3>
                <form id="inviteTeamForm" style="display:flex; gap:1rem; align-items:flex-end;">
                    <div style="flex:1;">
                        <label class="stat-label">Email Address</label>
                        <input type="email" id="inviteEmail" required style="width:100%; padding:0.5rem; background:rgba(255,255,255,0.05); border:1px solid var(--line); color:var(--ink);">
                    </div>
                    <div style="flex:1;">
                        <label class="stat-label">Role</label>
                        <select id="inviteRole" style="width:100%; padding:0.5rem; background:var(--paper-2); border:1px solid var(--line); color:var(--ink);">
                            <option value="TEAM_MEMBER">Team Member</option>
                            <option value="ADMIN">Admin</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn--accent" style="padding:0.6rem 1.2rem;">Send Invite</button>
                </form>
                <div id="inviteMsg" style="margin-top: 1rem; color: #4dff88;"></div>
            </div>
        `;

        html += `<div class="panel"><table class="data-table"><thead><tr><th>User ID</th><th>Venture</th><th>Role</th></tr></thead><tbody>`;
        
        if (!members || members.length === 0) {
            html += `<tr><td colspan="3">No team members found.</td></tr>`;
        } else {
            members.forEach(m => {
                html += `<tr>
                    <td>${m.user_id}</td>
                    <td>${m.ventures ? m.ventures.name : 'Unknown'}</td>
                    <td>${m.role}</td>
                </tr>`;
            });
        }
        
        html += `</tbody></table></div>`;
        mainContent.innerHTML = html;

        // Bind Invite form
        const form = document.getElementById('inviteTeamForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                document.getElementById('inviteMsg').innerText = "Mock Invite Sent to " + document.getElementById('inviteEmail').value;
            });
        }
    };

    const renderProjects = async () => {
        const { data: projects, error } = await window.supabaseClient
            .from('projects')
            .select('*, ventures(name)');
        if (error) throw error;

        let content = `<h2>Projects</h2>`;
        
        // Form to create new project (hidden if not admin/partner theoretically, but we rely on RLS to enforce)
        content += `
            <div class="panel" style="padding: 1.5rem; margin-bottom: 2rem;">
                <h3 style="margin-top:0;">Create Project</h3>
                <form id="createProjectForm" style="display:flex; gap:1rem; align-items:flex-end;">
                    <div style="flex:1;">
                        <label class="stat-label">Title</label>
                        <input type="text" id="newProjectTitle" required style="width:100%; padding:0.5rem; background:rgba(255,255,255,0.05); border:1px solid var(--line); color:var(--ink);">
                    </div>
                    <div style="flex:1;">
                        <label class="stat-label">Venture ID</label>
                        <input type="text" id="newProjectVenture" required style="width:100%; padding:0.5rem; background:rgba(255,255,255,0.05); border:1px solid var(--line); color:var(--ink);">
                    </div>
                    <button type="submit" class="btn btn--accent" style="padding:0.6rem 1.2rem;">Create</button>
                </form>
                <div id="projectMsg" style="margin-top: 1rem; color: #ff4d4d;"></div>
            </div>
        `;

        if (!projects || projects.length === 0) {
            content += emptyState('No active projects found for your ventures.');
        } else {
            content += `
                <div class="panel">
                    <table class="data-table">
                        <thead><tr><th>Project</th><th>Venture</th><th>Status</th><th>Actions</th></tr></thead>
                        <tbody>
                            ${projects.map(p => `
                                <tr>
                                    <td><strong>${p.title}</strong></td>
                                    <td>${p.ventures ? p.ventures.name : 'Unknown'}</td>
                                    <td>
                                        <select onchange="toggleProjectStatus('${p.id}', this.value)" style="background:var(--paper-2); color:var(--ink); border:1px solid var(--line); padding:0.25rem;">
                                            <option value="active" ${p.status === 'active' ? 'selected' : ''}>Active</option>
                                            <option value="pending" ${p.status === 'pending' ? 'selected' : ''}>Pending</option>
                                            <option value="archived" ${p.status === 'archived' ? 'selected' : ''}>Archived</option>
                                        </select>
                                    </td>
                                    <td>
                                        <button onclick="archiveProject('${p.id}')" style="background:none; border:none; color:#ff4d4d; cursor:pointer;">Archive</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }

        mainContent.innerHTML = content;

        // Bind form
        const form = document.getElementById('createProjectForm');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const title = document.getElementById('newProjectTitle').value;
                const venture_id = document.getElementById('newProjectVenture').value;
                const { error: insertError } = await window.supabaseClient.from('projects').insert([{ title, venture_id }]);
                if (insertError) {
                    document.getElementById('projectMsg').innerText = insertError.message;
                } else {
                    renderProjects(); // Refresh
                }
            });
        }
        
        // Bind Archive
        window.archiveProject = async (id) => {
            const { error: updateError } = await window.supabaseClient.from('projects').update({ status: 'archived' }).eq('id', id);
            if (updateError) {
                alert("Failed to archive: " + updateError.message);
            } else {
                renderProjects(); // Refresh
            }
        };

        // Bind Status Toggle
        window.toggleProjectStatus = async (id, newStatus) => {
            const { error: updateError } = await window.supabaseClient.from('projects').update({ status: newStatus }).eq('id', id);
            if (updateError) {
                alert("Failed to update status: " + updateError.message);
                renderProjects(); // revert visually
            }
        };
    };
    const renderDocuments = async () => {
        mainContent.innerHTML = emptyState('Loading documents...');
        
        try {
            const { data: documents, error } = await window.supabaseClient
                .from('documents')
                .select('*, ventures(name)');
            if (error) throw error;

            let content = `<h2>Documents</h2>`;

            // Upload form
            content += `
                <div class="panel" style="padding: 1.5rem; margin-bottom: 2rem;">
                    <h3 style="margin-top:0;">Upload Document</h3>
                    <form id="uploadDocForm" style="display:flex; flex-direction:column; gap:1rem;">
                        <div style="display:flex; gap:1rem; align-items:flex-end;">
                            <div style="flex:1;">
                                <label class="stat-label">File</label>
                                <input type="file" id="newDocFile" required style="width:100%; color:var(--ink);">
                            </div>
                            <div style="flex:1;">
                                <label class="stat-label">Venture ID</label>
                                <input type="text" id="newDocVenture" required style="width:100%; padding:0.5rem; background:rgba(255,255,255,0.05); border:1px solid var(--line); color:var(--ink);">
                            </div>
                            <button type="submit" id="uploadDocBtn" class="btn btn--accent" style="padding:0.6rem 1.2rem;">Upload</button>
                        </div>
                        <div id="docMsg" style="color: #ff4d4d; font-size:var(--fs-300);"></div>
                    </form>
                </div>
            `;

            if (!documents || documents.length === 0) {
                content += emptyState('No documents available for your ventures.');
            } else {
                content += `
                    <div class="panel">
                        <table class="data-table">
                            <thead><tr><th>Filename</th><th>Venture</th><th>Action</th></tr></thead>
                            <tbody>
                                ${documents.map(d => `
                                    <tr>
                                        <td><strong>${d.filename}</strong></td>
                                        <td>${d.ventures ? d.ventures.name : 'Unknown'}</td>
                                        <td>
                                            <button onclick="downloadDoc('${d.storage_path}')" style="background:none; border:none; color:var(--gold); cursor:pointer;">Download</button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }

            mainContent.innerHTML = content;

            const form = document.getElementById('uploadDocForm');
            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const msgEl = document.getElementById('docMsg');
                    const btn = document.getElementById('uploadDocBtn');
                    
                    const fileInput = document.getElementById('newDocFile');
                    const venture_id = document.getElementById('newDocVenture').value;
                    const file = fileInput.files[0];
                    if (!file) return;

                    btn.textContent = 'Uploading...';
                    btn.disabled = true;
                    msgEl.textContent = '';
                    msgEl.style.color = '#ff4d4d';

                    try {
                        // Sanitize inputs to prevent path traversal
                        const safeVentureId = venture_id.replace(/[^a-zA-Z0-9_-]/g, '');
                        const safeName = file.name.replace(/[\/\\:*?"<>|]/g, '_').replace(/\.\./g, '_');
                        if (!safeVentureId) throw new Error('Invalid venture ID');
                        const path = `${safeVentureId}/${Date.now()}_${safeName}`;
                        
                        // 1. Upload to storage
                        const { data: storageData, error: storageError } = await window.supabaseClient.storage
                            .from('private_documents')
                            .upload(path, file);
                            
                        if (storageError) throw storageError;

                        // 2. Insert metadata
                        const { error: dbError } = await window.supabaseClient
                            .from('documents')
                            .insert([{ filename: file.name, storage_path: path, venture_id: venture_id }]);
                            
                        if (dbError) throw dbError;

                        renderDocuments(); // refresh
                    } catch (err) {
                        msgEl.textContent = "Upload failed: " + err.message;
                        btn.textContent = 'Upload';
                        btn.disabled = false;
                    }
                });
            }

            window.downloadDoc = async (path) => {
                try {
                    const { data, error } = await window.supabaseClient.storage
                        .from('private_documents')
                        .download(path);
                    if (error) throw error;
                    
                    const url = URL.createObjectURL(data);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = path.split('/').pop();
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                } catch (err) {
                    alert("Download failed: " + err.message);
                }
            };
        } catch (err) {
            mainContent.innerHTML = `<div class="panel" style="padding: 2rem;"><p style="color:red;">Failed to load documents: ${err.message}</p></div>`;
        }
    };

    const renderReports = async () => {
        mainContent.innerHTML = emptyState('Loading reports...');
        try {
            // As an example report, we aggregate projects by status
            const { data: projects, error } = await window.supabaseClient.from('projects').select('status');
            if (error) throw error;
            
            if (!projects || projects.length === 0) {
                mainContent.innerHTML = emptyState('No data available to generate reports.');
                return;
            }

            const statusCounts = projects.reduce((acc, p) => {
                acc[p.status] = (acc[p.status] || 0) + 1;
                return acc;
            }, {});

            mainContent.innerHTML = `
                <h2>Reports</h2>
                <div class="panel">
                    <div class="panel-header">
                        <h3 class="panel-title">Project Distribution</h3>
                    </div>
                    <table class="data-table">
                        <thead><tr><th>Status</th><th>Count</th></tr></thead>
                        <tbody>
                            ${Object.entries(statusCounts).map(([status, count]) => `
                                <tr>
                                    <td><strong>${status.toUpperCase()}</strong></td>
                                    <td>${count}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } catch (err) {
            mainContent.innerHTML = `<div class="panel" style="padding: 2rem;"><p style="color:red;">Failed to generate reports: ${err.message}</p></div>`;
        }
    };
    const renderSettings = async () => {
        mainContent.innerHTML = emptyState('Loading settings...');
        try {
            const { data: { session } } = await window.supabaseClient.auth.getSession();
            if (!session) return;

            const { data: profile } = await window.supabaseClient
                .from('profiles')
                .select('role, created_at')
                .eq('id', session.user.id)
                .single();

            const userRole = profile ? profile.role : 'Unknown';
            const createdAt = profile && profile.created_at
                ? new Date(profile.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
                : 'Unknown';

            mainContent.innerHTML = `
                <h2>Settings</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-label">Email</span>
                        <div style="font-size: var(--fs-500); color: var(--ink);">${session.user.email}</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-label">Role</span>
                        <div style="font-size: var(--fs-500); color: var(--gold);">${userRole}</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-label">Member Since</span>
                        <div style="font-size: var(--fs-500); color: var(--ink);">${createdAt}</div>
                    </div>
                </div>
                <div class="panel" style="padding: 1.5rem; margin-top: 2rem;">
                    <h3 style="margin-top:0;">Change Password</h3>
                    <form id="settingsPasswordForm" style="display:flex; gap:1rem; align-items:flex-end; max-width: 500px;">
                        <div style="flex:1;">
                            <label class="stat-label">New Password</label>
                            <input type="password" id="settingsNewPwd" required minlength="8"
                                style="width:100%; padding:0.5rem; background:rgba(255,255,255,0.05); border:1px solid var(--line); color:var(--ink); border-radius: var(--radius-sm); box-sizing: border-box;">
                        </div>
                        <button type="submit" class="btn btn--accent" style="padding:0.6rem 1.2rem;">Update</button>
                    </form>
                    <div id="settingsPwdMsg" style="margin-top: 1rem; font-size: var(--fs-300);"></div>
                </div>
            `;

            const form = document.getElementById('settingsPasswordForm');
            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const msgEl = document.getElementById('settingsPwdMsg');
                    const newPwd = document.getElementById('settingsNewPwd').value;
                    msgEl.textContent = '';
                    msgEl.style.color = '#4dff88';
                    try {
                        const { error } = await window.supabaseClient.auth.updateUser({ password: newPwd });
                        if (error) throw error;
                        msgEl.textContent = 'Password updated successfully.';
                        document.getElementById('settingsNewPwd').value = '';
                    } catch (err) {
                        msgEl.style.color = '#ff4d4d';
                        msgEl.textContent = 'Failed: ' + err.message;
                    }
                });
            }
        } catch (err) {
            mainContent.innerHTML = `<div class="panel" style="padding: 2rem;"><p style="color:red;">Failed to load settings: ${err.message}</p></div>`;
        }
    };

    // Initialize Router
    route();

    // Hook up sidebar clicks to the router
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(link => {
        const text = link.textContent.trim().toLowerCase();
        link.setAttribute('href', `#${text}`);
    });
});
