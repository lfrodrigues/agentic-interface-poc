import time
import json
from django.utils.deprecation import MiddlewareMixin

class RequestLoggerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Store the start time for calculating request duration
        request.start_time = time.time()

    def process_response(self, request, response):
        # return response 

        # Calculate request duration
        duration = time.time() - getattr(request, 'start_time', 0)
        
        # Get request body for POST/PUT requests
        body = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = json.loads(request.body)
            except:
                body = request.POST or request.body

        # Get response content
        try:
            response_content = response.content.decode('utf-8')
        except:
            response_content = '[Binary Response]'

        # Log request details
        print(f"\n{'='*80}")
        print(f"Request Details:")
        print(f"{'='*80}")
        print(f"Method: {request.method}")
        print(f"Path: {request.path}")
        print(f"Query Params: {dict(request.GET)}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        print(f"User Agent: {request.META.get('HTTP_USER_AGENT', 'N/A')}")
        print(f"IP Address: {request.META.get('REMOTE_ADDR', 'N/A')}")
        print(f"Content Type: {request.META.get('CONTENT_TYPE', 'N/A')}")
        
        print(f"\nHeaders:")
        print(f"{'-'*80}")
        for header, value in request.META.items():
            if header.startswith('HTTP_'):
                print(f"{header}: {value}")
        
        if body:
            print(f"\nRequest Body:")
            print(f"{'-'*80}")
            print(json.dumps(body, indent=2))
        
        print(f"\nResponse:")
        print(f"{'-'*80}")
        print(response_content[:1000] + '...' if len(response_content) > 1000 else response_content)
        print(f"{'='*80}\n")
        
        return response 