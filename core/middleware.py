import traceback
from django.shortcuts import render
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
