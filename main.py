from app import create_app, db
from flask_wtf.csrf import CSRFProtect

app = create_app()

# Secure Session Cookies (Ensure cookies are only sent over HTTPS)
app.config.update(
    SESSION_COOKIE_SECURE=True,  # Ensure cookies are only sent over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE="Strict",  # Restrict cross-site cookie sharing
)

# Enable CSRF Protection
csrf = CSRFProtect(app)

# Apply Security Headers After Each Request
@app.after_request
def add_security_headers(response):
    # Clickjacking Prevention
    response.headers["X-Frame-Options"] = "DENY"
    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Enforce HTTPS
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Content Security Policy (CSP)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; object-src 'none';"
    # Restrict browser features
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    # Prevent Spectre-like attacks
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    return response

if __name__ == "__main__":
    app.run(debug=True)

