from datetime import date

from django.conf import settings

from .models import Partner


def partners(request):
    return {
        'partners': Partner.objects.filter(is_active=True).order_by('order', 'name')
    }


# Single source of truth for the organisation's headline facts.
#
# These were previously hardcoded in several templates and had drifted out of
# sync — the homepage simultaneously claimed "over a decade", "2017 / over 7
# years" and "a septennium". Change them here and every page follows.
FOUNDED_YEAR = 2015
REGISTERED_YEAR = 2017
RANGERS_TRAINED = 500
HECTARES_PROTECTED = 50000
DEPLOYMENT_LOCATIONS = 8


def navigation(request):
    """Menu data for the header.

    The course and location menus were hardcoded lists in base.html that had
    drifted from the database — the locations menu named five towns while nine
    sites existed. Building them from the data keeps the menu honest.
    """
    from .models import Course, DeploymentLocation

    # One query for the types that actually have active courses, rather than
    # an exists() check per type.
    populated = set(
        Course.objects.filter(is_active=True)
        .values_list('course_type', flat=True)
        .distinct()
    )

    return {
        'nav_course_types': [
            {'slug': value.lower(), 'label': label}
            for value, label in Course.COURSE_TYPES
            if value in populated
        ],
        'nav_locations': DeploymentLocation.objects.order_by('name')[:8],
    }


def site_facts(request):
    years_operating = date.today().year - FOUNDED_YEAR
    return {
        'site_facts': {
            'founded_year': FOUNDED_YEAR,
            'registered_year': REGISTERED_YEAR,
            'years_operating': years_operating,
            'rangers_trained': RANGERS_TRAINED,
            'hectares_protected': f'{HECTARES_PROTECTED:,}',
            'deployment_locations': DEPLOYMENT_LOCATIONS,
            'contact_email': settings.CONTACT_RECIPIENT,
        }
    }
