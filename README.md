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

## 🔍 Technical SEO & AI Search Optimization (New)

The project features standard-compliant **Google-grade technical search engine optimization (SEO)** and is fully prepared for generative AI search engines (such as Google AI Overview, ChatGPT search, Perplexity AI, and Gemini):

*   **🤖 Automated Search Crawler Whitelist (`BotProtectionMiddleware`)**: Bypasses security checks for certified search engines and AI crawl bots (like `Googlebot`, `Bingbot`, `Applebot`, `GPTBot`, `PerplexityBot`, etc.), ensuring zero crawling restrictions while keeping scanner protection robust.
*   **🗺️ Dynamic Runtime Sitemap Feed (`/sitemap.xml`)**: Generates structured dynamic sitemaps instantly at runtime with correct page priorities, keeping search indexes fully synchronized.
*   **📄 Dynamic Crawler Directives (`/robots.txt`)**: Explicitly controls search indexes, provides sitemap directions, and blocks automated scans of private directories like `/custom-admin/`.
*   **🏷️ Dynamic Metadata Head Injector**: Employs dynamic server-rendered `<title>` and `<meta name="description">` blocks matching active routes during initial loading.
*   **🔗 Canonical URL Tags**: Injects explicit canonical link headers to prevent duplicate-content indexing penalties.
*   **🌐 Premium OpenGraph & Twitter Cards**: Leverages high-definition social open graphs for rich preview cards when links are shared on LinkedIn, WhatsApp, Twitter/X, and Slack.
*   **🗂️ Rich JSON-LD Structured Graph Schema**: Delivers comprehensive structural data schemas including **Person** (expertise, credentials, and social indicators), **WebSite** properties, and local **ProfessionalService** descriptors directly to crawler algorithms.
*   **🔑 Dynamic Google Verification Token (`/google[verification_hash].html`)**: Employs a dynamic backend router that automatically serves the Google Search Console verification token without requiring manual uploading of static HTML files to Render, keeping production clean.

---

## 📊 Advanced Analytics & Global Settings Engine (New)

The website features a production-grade, privacy-respecting analytics suite and database-driven global settings configuration:

*   **📈 Dynamic Portfolio Global Stats (`SiteSettings`)**: The landing page (Hero section) and the About page stats are fully database-driven and synchronized in real-time. You can control `Projects Count`, `Satisfaction Rate`, and `Experience Years` directly from the Custom Admin settings dashboard without redeploying code.
*   **👥 Device-Level Unique Visitor Tracking**: Enforces high-fidelity unique user tracking using secure `device_id` cookie identifiers:
    - Automatically generates and assigns a cryptographically secure UUID token on a user's initial visit.
    - Persists the unique device identity across sessions via `HTTPOnly` and `SameSite=Lax` cookies.
*   **🗄️ Lifetime Visitor Analytics (`UniqueVisitor` Model)**: Records lifetime unique device interactions inside a dedicated database cache:
    - Captures the exact timestamp of their `first_visited` and `last_visited` interactions.
    - Counts cumulative interactions (`visit_count`) per device to distinguish between new and recurring visitors.
*   **🤖 Silent Bot & Uptime Monitor Filtering**: Automatically screens incoming user-agents to filter out monitoring pings and automated crawls (like `UptimeRobot`, `Pingdom`, `Better Uptime`, `StatusCake`, `Googlebot`, custom HTTP scripts, etc.) from counting toward your analytics:
    - **No Request Blocking:** Automated monitoring requests are served a complete `HTTP 200 OK` HTML render to prevent your hosting environment (like Render) from sleeping or spinning down.
    - **No Analytics Pollution:** Database insertion of logs and unique visitor increments are completely bypassed for bots, keeping your database compact, clean, and highly performant.
*   **🎨 Live Stats Monitor**: Displays real-time "Total Views", "Unique Visitors", and "Views Today" beautifully inside the Admin Dashboard using harmonized color palettes and responsive layouts.
*   **🔄 Zero-Ops Historical Data Backfill Migration (`0013_backfill_unique_visitors`)**: Automatically recovers and updates historical analytics logs from past deployments on first startup. It groups past visits by their User-Agent footprint, generates deterministic UUID device keys, and populates the `UniqueVisitor` model safely without requiring any manual terminal commands on Render.

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

--