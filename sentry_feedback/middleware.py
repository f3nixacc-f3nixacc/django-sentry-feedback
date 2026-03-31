from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse


class SentryFeedbackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.dsn = getattr(settings, 'SENTRY_FEEDBACK_DSN', '')

    def __call__(self, request):
        response = self.get_response(request)

        if not self._should_inject(request, response):
            return response

        content = response.content.decode(response.charset)
        widget_html = render_to_string('sentry_feedback/widget.html', {
            'sentry_feedback_dsn': self.dsn,
            'sentry_feedback_user_name': request.user.get_full_name() or request.user.username,
            'sentry_feedback_user_email': getattr(request.user, 'email', ''),
        }, request=request)

        content = content.replace('</body>', widget_html + '</body>')
        response.content = content.encode(response.charset)
        response['Content-Length'] = len(response.content)
        return response

    def _should_inject(self, request, response):
        if not self.dsn:
            return False
        if response.status_code != 200:
            return False
        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return False
        if not hasattr(response, 'content'):
            return False
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return False
        if not request.user.is_staff:
            return False
        try:
            admin_prefix = reverse('admin:index')
        except Exception:
            admin_prefix = '/admin/'
        if not request.path.startswith(admin_prefix):
            return False
        return True
