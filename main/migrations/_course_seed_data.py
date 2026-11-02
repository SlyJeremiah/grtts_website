"""Course content shared by the seeding migrations.

Django's migration loader ignores modules whose name starts with an
underscore, so this sits beside the migrations without being treated as one.
It holds the course content that used to be hardcoded in
main/templates/main/courses.html, so 0008 and 0009 cannot drift apart.
"""

COURSES = [
    {
        'title': 'Basic Ranger Course',
        'course_type': 'BASIC',
        'duration': '6 Weeks',
        'intake_dates': 'January, June, October',
        'description': (
            'Conservation Guardianship.\n\n'
            'Detailed entry level studies for individuals aspiring to join the '
            'field of wildlife protection and anti-poaching operations.'
        ),
    },
    {
        'title': 'Advanced Ranger & Patrol',
        'course_type': 'ADVANCED',
        'duration': '2 Weeks',
        'intake_dates': 'March, November',
        'description': 'Designed for rangers moving into leadership roles.',
    },
    {
        'title': 'Basic Tracking Course',
        'course_type': 'TRACKING',
        'duration': '7 Days',
        'intake_dates': 'Available on request',
        'description': (
            'Held at Victoria Falls, in a Big 5 area.\n\n'
            'The course covers:\n'
            '- Signs of the wild\n'
            '- The art of human and wildlife tracking\n'
            '- Tracking as a science\n'
            '- Track and sign identification\n'
            '- Trailing\n'
            '- Tracking evaluation\n\n'
            'Accommodation: tents are provided. Participants bring their own '
            'personal gear.'
        ),
    },
    {
        'title': 'Tracking: Basic, Advanced & Counter-Insurgency',
        'course_type': 'SPECIALIST',
        'duration': 'Varies by level',
        'intake_dates': 'Available all year round',
        'description': (
            'Specialist tracking instruction across basic, advanced and '
            'counter-insurgency disciplines.'
        ),
    },
    {
        'title': 'Small Team Tactics',
        'course_type': 'SPECIALIST',
        'duration': 'Varies by requirement',
        'intake_dates': 'Available all year round',
        'description': (
            'Specialist training in small team movement, formations and '
            'field tactics for anti-poaching units.'
        ),
    },
    {
        'title': 'K9 Handling & Kennel Management',
        'course_type': 'SPECIALIST',
        'duration': 'Varies by requirement',
        'intake_dates': 'Available all year round',
        'description': (
            'Specialist training in the handling, deployment and kennel '
            'management of anti-poaching working dogs.'
        ),
    },
]
