
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    age_treatment = models.StringField(choices=[['18-25', '18-25'], ['26-36', '26-36'], ['37-47', '37-47'], ['48-59', '48-59'], ['60 or above', '60 or above']], label='Which age group do you belong to?')
    income = models.StringField(choices=[['$0-$14,999/year', '$0-$14,999/year'], ['$15,000-$29,999/year', '$15,000-$29,999/year'], ['$30,000-$44,999/year', '$30,000-$44,999/year'], ['$45,000–$64,999/year', '$45,000–$64,999/year'], ['$65,000-$89,999/year', '$65,000-$89,999/year'], ['$90,000 or above', '$90,000 or above']], label='What is your income?')
class Consent(Page):
    form_model = 'player'
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age_treatment', 'income']
page_sequence = [Consent, Demographics]