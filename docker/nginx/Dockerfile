FROM nginx:1.25-alpine

# Remove the default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for custom error pages
RUN mkdir -p /usr/share/nginx/html

# Health check configuration
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost/health || exit 1

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
