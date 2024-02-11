from os import environ

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, 
    participation_fee=0,
)

SESSION_CONFIGS = [
    dict(
        name='my_session', 
        num_demo_participants=2, 
        app_sequence=['consent', 'general_knowledge_quiz', 'zgamble_game'],
    ),
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['quiz_payment']  # Add this if you plan to record cumulative participant-specific fields across apps
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'CHANGE_ME')  # Fallback to 'CHANGE_ME' if environment variable is not set

SECRET_KEY = 'blahblah'

INSTALLED_APPS = ['otree']