from rest_framework.response import Response


class SuccessCreatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        is_api = request.path.startswith("/api/")
        if is_api and isinstance(response, Response) and (201 == response.status_code):
            response.data = {
                "message": "xona muvaffaqiyatli band qilindi"
            }
            response._is_rendered = False
            response.render()

        return response
