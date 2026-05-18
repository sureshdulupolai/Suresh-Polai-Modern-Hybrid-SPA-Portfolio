# 🚀 Suresh Polai – Modern Hybrid SPA Portfolio

A high-performance personal portfolio built using **Django 5 (Python)** with a modern interactive frontend powered by **Tailwind CSS, Vanilla JavaScript, Three.js, and GSAP**.

This project follows a **Hybrid Single Page Application (SPA)** architecture — combining Django server-side rendering (for SEO & fast initial load) with AJAX-based dynamic partial rendering (for smooth navigation without full page reload).

---

## 🛡️ Security Hardening & Hacker Protection (New)

The project has been upgraded to a **Hacker-Resistant, Production-Grade** status with a highly customized stack of automated defensive middlewares and secure configurations:

*   **🤖 Bot & Vulnerability Scanner Blocker (`BotProtectionMiddleware`)**: Scans incoming headers and instantly terminates requests from common scanners, bad crawlers, and offensive tools (like `sqlmap`, `nikto`, `nmap`, `masscan`, `zgrab`, `acunetix`, `dirbuster`, `gobuster`, etc.) with a `403 Forbidden` response.
*   **⚡ IP Rate Limiter (`RateLimitMiddleware`)**: Enforces a dynamic sliding-window rate limiter powered by Django's local cache. It automatically blocks brute-force credentials flooding and spam submissions:
    - `/custom-admin/login/`: Max **5 requests per minute** (POST only).
    - `/custom-admin/signup/`: Max **3 requests per minute** (POST only).
    - `/contact/submit/`: Max **2 submissions per minute** (POST only).
    - Exceeded requests automatically receive a clean `429 Too Many Requests` status.
*   **🛡️ Hardened Security Response Headers (`SecurityHeadersMiddleware`)**: Injects high-grade security flags on every response to control client-side browser behavior:
    - `X-Content-Type-Options: nosniff` (Defeats MIME-sniffing exploits)
    - `X-Frame-Options: DENY` (Blocks framing, iframe manipulation, and clickjacking)
    - `X-XSS-Protection: 1; mode=block` (Enforces modern XSS filtering)
    - `Referrer-Policy: strict-origin-when-cross-origin` (Protects metadata exposure)
    - `Permissions-Policy: geolocation=()` (Limits hardware access vectors)
*   **🍪 XSS Mitigation Cookies**: Enforces standard `HTTPOnly` and `SameSite=Lax` cookies for both sessions and CSRF tokens by default, preventing JavaScript from reading or extracting credentials.
*   **🔒 Live environment (Render) SSL/HSTS**: If running on Render, the system automatically redirects HTTP to HTTPS (`SECURE_SSL_REDIRECT = True`), activates `SECURE` session and CSRF cookies, and sets a strict **1-year HTTP Strict Transport Security (HSTS)** envelope with subdomains and preload inclusion.

---

## 🛠️ Dynamic Database Environment Selector (New)

The system automatically detects your environment using environment variables (like `RENDER=true` or `DATABASE_URL`):
- **Local Development:** Falls back to a local SQLite database (`db.sqlite3`), ensuring zero impact on the live database.
- **Production (Render):** Dynamically parses and connects to your live PostgreSQL database using `dj_database_url` for seamless, robust operations.

---

## 📂 Interactive Project Ordering Engine (New)

- **Interactive Sort Inputs:** Added a dedicated **Sort Order** number input field next to each project in the custom admin panel.
- **"Save Ordering" Button:** Features a green **Save Ordering** button at the top that remains **disabled by default** and **instantly activates** only when you change at least one sorting value, preventing duplicate/accidental requests.
- **Save Spinner:** Morphs into a dynamic loading spinner showing *"Saving..."* when clicked to prevent double-submitting.
- **Valid HTML5 Layout:** Relocated deletion forms safely outside the main table form to prevent nested form tags, keeping HTML completely standard-compliant.
- **Explicit Sort Order:** Projects display on the public page in the exact sorting order defined (`1` for first, `2` for second, and so on) with `created_at` as a fallback.

---

## 🔥 Key Features

- ⚡ **Hybrid SPA Architecture** (SEO-friendly initial load + AJAX dynamic content updates)
- 🎨 **Modern UI** built with Tailwind CSS and glassmorphism styling
- 🌌 **3D Animated Background** using Three.js particles
- 🎬 **Advanced animations** with GSAP
- 🌙 **Dark Mode** with local storage persistence
- 🛠 **Custom Admin Panel** (A tailored dashboard for managing content, bypassing default Django admin)
- 📊 **Built-in Analytics Tracking** (`SiteVisit` model) to monitor unique visits and traffic sources
- 📩 **Secure Contact Form** with device fingerprinting and rate-limiting to prevent spam
- 📱 **Fully Responsive Design** with custom floating pill navbar spacing

---

## 🏛️ Repository Architecture

```text
portfolio_n/
├── config/                 # Root Django configuration directory
│   ├── settings.py         # Production-hardened settings (DB selector, CSRF, HSTS, CSP)
│   └── urls.py             # Centralized route controllers
├── core/                   # Main application logic
│   ├── middleware.py       # Custom defensive stack (Rate limits, Bot protection, Headers)
│   ├── models.py           # Database tables (Project, Experience, Skill, SiteVisit, etc.)
│   ├── views.py            # SPA shell rendering and contact submit APIs
│   └── urls.py             # Public navigation endpoints
├── custom_admin/           # Tailored admin dashboard app (CRUD and Analytics)
├── templates/              # HTML templates (SPA container, Admin portal, custom 500 error page)
├── static/                 # Static assets (Tailwind tokens, Three.js backgrounds, GSAP scripts)
├── manage.py               # Django CLI controller
└── requirements.txt        # Hardened package requirements
```

---

## 🚀 How to Run

1.  **Activate Environment** (if applicable):
    ```bash
    env\Scripts\activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Start Server**:
    ```bash
    python manage.py runserver
    ```
5.  **Access**: Open `http://127.0.0.1:8000/`
