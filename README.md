# django-sentry-feedback

Drop-in Sentry user feedback widget for Django admin with [Unfold](https://github.com/unfoldadmin/django-unfold) theme support. Adds a floating feedback button to every admin page. Users can describe issues, capture page screenshots, and submit directly to Sentry — no JS SDK required.

## Features

- Floating feedback button on all admin pages (staff users only)
- Page screenshot capture via html2canvas-pro (supports modern CSS: oklch, oklab, color-mix)
- File attachment support (manual image upload)
- Direct submission to Sentry Envelope API (no Sentry JS SDK dependency)
- Dark / light theme — follows Unfold's theme toggle
- Responsive — full-width panel on mobile
- Auto-fills user name and email from Django auth
- Zero external runtime dependencies (html2canvas bundled as static file)

## Requirements

- Python 3.10+
- Django 4.2+
- [django-unfold](https://github.com/unfoldadmin/django-unfold) (any version)
- Sentry project with DSN

## Installation

```bash
pip install git+https://github.com/f3nixacc-f3nixacc/django-sentry-feedback.git@v0.1.0
```

Or add to `requirements.txt`:

```
django-sentry-feedback @ git+https://github.com/f3nixacc-f3nixacc/django-sentry-feedback.git@v0.1.0
```

## Configuration

Add **4 changes** to your `settings.py`:

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'sentry_feedback',        # <-- add after unfold
    'django.contrib.admin',
    # ...
]
```

### 2. Add middleware (last position)

```python
MIDDLEWARE = [
    # ... all your middleware ...
    'sentry_feedback.middleware.SentryFeedbackMiddleware',  # <-- add last
]
```

### 3. Add context processor

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... existing processors ...
                'sentry_feedback.context_processors.sentry_feedback_context',  # <-- add
            ],
        },
    },
]
```

### 4. Set Sentry DSN

```python
# Reuse your existing SENTRY_DSN env variable
SENTRY_FEEDBACK_DSN = env('SENTRY_DSN')  # or os.environ.get('SENTRY_DSN', '')
```

### 5. Collect static files

```bash
python manage.py collectstatic --noinput
```

That's it. Open any admin page — the feedback button appears in the bottom-right corner for staff users.

## How it works

1. **Middleware** checks every response: is it HTML? is the user staff? is the path under `/admin/`?
2. If yes, renders `widget.html` and injects it before `</body>`
3. **Widget** is a self-contained HTML + CSS + JS block (no external requests at runtime)
4. **Screenshot** uses [html2canvas-pro](https://github.com/nicolo-ribaudo/html2canvas-pro) loaded from local static files
5. **Submission** builds a [Sentry Envelope](https://develop.sentry.dev/sdk/envelopes/) with the feedback event + optional screenshot attachment, and POSTs it directly to `https://{host}/api/{project}/envelope/` using the public DSN key

## Configuration reference

| Setting | Required | Description |
|---------|----------|-------------|
| `SENTRY_FEEDBACK_DSN` | Yes | Sentry DSN (public key). The widget won't render if empty. |

The DSN is a public key — safe to include in frontend HTML. It only allows sending events, not reading data.

## Alternative: Template tag (manual placement)

Instead of (or alongside) the middleware, you can use the template tag for explicit control:

```html
{% load sentry_feedback %}

{# Place anywhere in your template #}
{% sentry_feedback_widget %}
```

## Compatibility

Tested with:

| Component | Versions |
|-----------|----------|
| Django | 5.1 — 5.2 |
| django-unfold | 0.63 — 0.70 |
| Sentry | SaaS (sentry.io, regional endpoints) |
| Browsers | Chrome 90+, Firefox 90+, Safari 15+, Edge 90+ |
| CSS | oklch, oklab, color-mix (Tailwind v4) |

## License

MIT
