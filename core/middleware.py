from django.shortcuts import render
from django.http import Http404
from .models import ErrorLog

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the error to the database
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
