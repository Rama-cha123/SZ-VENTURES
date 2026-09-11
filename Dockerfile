# ─────────────────────────────────────────────────────────────────────────────
# SZX Ventures — Dockerfile
# Serves the static site with Nginx (Alpine), production-hardened.
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Minimal Nginx on Alpine ─────────────────────────────────────────
FROM nginx:1.27-alpine AS production

# Labels
LABEL org.opencontainers.image.title="szx-ventures"
LABEL org.opencontainers.image.description="SZX Ventures static website"
LABEL org.opencontainers.image.source="https://github.com/your-org/szx-ventures"

# Remove default nginx html and configs
RUN rm -rf /usr/share/nginx/html/* /etc/nginx/conf.d/*

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the entire static site
COPY . /usr/share/nginx/html/

# Remove files that should not be served
RUN rm -f /usr/share/nginx/html/Dockerfile \
          /usr/share/nginx/html/nginx.conf \
          /usr/share/nginx/html/.gitignore \
          /usr/share/nginx/html/.github \
          /usr/share/nginx/html/vendor-aos \
          /usr/share/nginx/html/vendor-lenis \
          /usr/share/nginx/html/vendor-tippy \
          /usr/share/nginx/html/vendor-odometer \
          /usr/share/nginx/html/vendor-swup \
          /usr/share/nginx/html/ui-ux-pro-max-skill && true

# Set proper file permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Nginx runs on port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
