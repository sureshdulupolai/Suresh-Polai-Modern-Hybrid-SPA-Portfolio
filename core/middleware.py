from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.cache import cache
from .models import ErrorLog
import traceback
import time
import re

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Ignore standard Http404 exceptions and let Django's core 404 handler handle it
        if isinstance(exception, Http404):
            return None

        # Log standard exceptions to the database
        ErrorLog.objects.create(
            path=request.path,
            method=request.method,
            error_message=str(exception),
            traceback=traceback.format_exc()
        )
        
        # Return a custom 500 error page
        return render(request, '500.html', status=500)

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path starts with /custom-admin/
        if request.path.startswith('/custom-admin/'):
            # Define public admin paths
            public_paths = [
                '/custom-admin/login/',
                '/custom-admin/signup/',
            ]
            
            # If path is not public and user is not an authenticated superuser, raise 404
            if request.path not in public_paths:
                if not request.user.is_authenticated or not request.user.is_superuser:
                    raise Http404("Page not found")
        
        response = self.get_response(request)
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        
        # Define limits (max_requests, period_in_seconds) per POST endpoint
        limits = {
            '/custom-admin/login/': (5, 60),      # max 5 requests per 60s
            '/custom-admin/signup/': (3, 60),     # max 3 requests per 60s
            '/contact/submit/': (2, 60),          # max 2 contact submissions per 60s
        }
        
        for limit_path, (max_requests, period) in limits.items():
            if path.startswith(limit_path) and request.method == 'POST':
                cache_key = f"rate_limit_{ip}_{limit_path}"
                request_timestamps = cache.get(cache_key, [])
                
                current_time = time.time()
                request_timestamps = [t for t in request_timestamps if current_time - t < period]
                
                if len(request_timestamps) >= max_requests:
                    response_html = (
                        "<html><head><title>Too Many Requests</title>"
                        "<style>body { font-family: sans-serif; text-align: center; padding: 100px; background: #0f172a; color: #cbd5e1; }"
                        "h1 { color: #f43f5e; } p { font-size: 18px; }</style></head>"
                        "<body><h1>429 Too Many Requests</h1>"
                        "<p>Brute-force protection triggered. Please wait a minute before trying again.</p></body></html>"
                    )
                    return HttpResponse(response_html, status=429)
                
                request_timestamps.append(current_time)
                cache.set(cache_key, request_timestamps, period)
                
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class BotProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile regular expression for bad bots, web scanners, and common vulnerability tools
        self.bot_regex = re.compile(
            r'(sqlmap|nikto|nmap|masscan|zgrab|acunetix|dirbuster|gobuster|w3af|netsparker|hydra|zaproxy|commix|arachni|n-stealth|scrapy|ahrefsbot|semrushbot)',
            re.IGNORECASE
        )

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if user_agent and self.bot_regex.search(user_agent):
            return HttpResponseForbidden("Access Denied: Security Scanner or Unapproved User Agent Detected.")
        return self.get_response(request)

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=()'
        return response
