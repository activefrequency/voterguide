from django.conf import settings

def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS_PROPERTY_ID': getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', ''),
        'GOOGLE_ANALYTICS_DOMAIN': getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', ''),
    }

def branding(request):
    return {
        'BRANDING': settings.VOTERGUIDE_SETTINGS['BRANDING'],
    }
