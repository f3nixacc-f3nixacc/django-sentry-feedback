from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('sentry_feedback/widget.html', takes_context=True)
def sentry_feedback_widget(context):
    request = context.get('request')
    dsn = getattr(settings, 'SENTRY_FEEDBACK_DSN', '')

    if not request or not dsn:
        return {'sentry_feedback_dsn': ''}

    user = request.user
    return {
        'sentry_feedback_dsn': dsn,
        'sentry_feedback_user_name': user.get_full_name() or user.username if user.is_authenticated else '',
        'sentry_feedback_user_email': getattr(user, 'email', '') if user.is_authenticated else '',
    }
