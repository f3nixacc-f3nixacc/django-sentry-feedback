from django.conf import settings


def sentry_feedback_context(request):
    dsn = getattr(settings, 'SENTRY_FEEDBACK_DSN', '')
    if not dsn or not hasattr(request, 'user') or not request.user.is_authenticated:
        return {}

    user = request.user
    return {
        'sentry_feedback_dsn': dsn,
        'sentry_feedback_user_name': user.get_full_name() or user.username,
        'sentry_feedback_user_email': getattr(user, 'email', ''),
    }
