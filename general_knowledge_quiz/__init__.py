
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'general_knowledge_quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWERS = {
    'q1': 'd. Condoleezza Rice',
    # 'q2': 'a. Pittsburg Steelers',
    # 'q3': 'a. California',
    # 'q4': 'a. John Kennedy',
    # 'q5': 'c. Albany',
    # 'q6': 'b. Virginia',
    # 'q7': 'c. Jeff Probst',
    # 'q8': 'd. Teddy bear',
    # 'q9': 'd. Smokey the Bear',
    # 'q10': 'd. Great Britain',
    # 'q11': 'c. The Parent Trap',
    # 'q12': 'a. Fox',
    # 'q13': 'b. a hospital',
    # 'q14': 'c. Thomas Edison',
    # 'q15': 'd. North Carolina',
}
    
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    score = models.IntegerField(initial=0)
    payment = models.CurrencyField(initial=0)
    q1 = models.StringField(choices=[['a. Dick Cheney', 'a. Dick Cheney'], ['b. John Snow', 'b. John Snow'], ['c. Donald Rumsfeld', 'c. Donald Rumsfeld'], ['d. Condoleezza Rice', 'd. Condoleezza Rice']], label='The current Secretary of State is')
    # q2 = models.StringField(choices=[['a. Pittsburg Steelers', 'a. Pittsburg Steelers'], ['b. Indianapolis Colts', 'b. Indianapolis Colts'], ['c. Carolina Panthers', 'c. Carolina Panthers'], ['d. Seattle Seahawks', 'd. Seattle Seahawks']], label='The winner of the 2006 Superbowl was')
    # q3 = models.StringField(choices=[['a. California', 'a. California'], ['b. Texas', 'b. Texas'], ['c. Maine', 'c. Maine'], ['d. North Carolina', 'd. North Carolina']], label='Which of the following states borders the Gulf of Mexico?')
    # q4 = models.StringField(choices=[['a. John Kennedy', 'a. John Kennedy'], ['b. Bill Clinton', 'b. Bill Clinton'], ['c. Gerald Ford', 'c. Gerald Ford'], ['d. Ronald Reagan', 'd. Ronald Reagan']], label='Who was the last President to die in office?')
    # q5 = models.StringField(choices=[['a. Pierre', 'a. Pierre'], ['b. Sacramento', 'b. Sacramento'], ['c. Albany', 'c. Albany'], ['d. Little Rock', 'd. Little Rock']], label='What is the capital of Arkansas?')
    # q6 = models.StringField(choices=[['a. Montana', 'a. Montana'], ['b. Virginia', 'b. Virginia'], ['c. Louisiana', 'c. Louisiana'], ['d. Texas', 'd. Texas']], label='Which of the following was one of the first 13 colonies?')
    # q7 = models.StringField(choices=[['a. Howie Mandel', 'a. Howie Mandel'], ['b. Regis Philbin', 'b. Regis Philbin'], ['c. Jeff Probst', 'c. Jeff Probst'], ['d. Ryan Seacrest', 'd. Ryan Seacrest']], label='Who is the host of American Idol?')
    # q8 = models.StringField(choices=[['a. Jacks', 'a. Jacks'], ['b. Raggedy Andy', 'b. Raggedy Andy'], ['c. Marco Polo', 'c. Marco Polo'], ['d. Teddy bear', 'd. Teddy bear']], label='Which of the following toys was named for a U.S. President?')
    # q9 = models.StringField(choices=[['a. Toucan Sam', 'a. Toucan Sam'], ['b. Polly the Parrot', 'b. Polly the Parrot'], ['c. Woodsy the Owl', 'c. Woodsy the Owl'], ['d. Smokey the Bear', 'd. Smokey the Bear']], label='"Only you can prevent forest fires.” was the slogan of')
    # q10 = models.StringField(choices=[['a. Germany', 'a. Germany'], ['b. Switzerland', 'b. Switzerland'], ['c. Italy', 'c. Italy'], ['d. Great Britain', 'd. Great Britain']], label='Which of the following was an ally of the United States in World War II?')
    # q11 = models.StringField(choices=[['a. Freaky Friday', 'a. Freaky Friday'], ['b. The Pajama Game', 'b. The Pajama Game'], ['c. The Parent Trap', 'c. The Parent Trap'], ['d. Yours, Mine and Ours', 'd. Yours, Mine and Ours']], label='Which of the following is a movie about twin girls raised separately who meet at camp and eventually persuade their parents to reunite?')
    # q12 = models.StringField(choices=[['a. Fox', 'a. Fox'], ['b. PBS', 'b. PBS'], ['c. HBO', 'c. HBO'], ['d. MTV', 'd. MTV']], label=' Which television network carries the OC?')
    # q13 = models.StringField(choices=[['a. a carwash', 'a. a carwash'], ['b. a hospital', 'b. a hospital'], ['c. a baseball team', 'c. a baseball team'], ['d. hotel maid service', 'd. hotel maid service']], label='“Scrubs” is a television series centered around')
    # q14 = models.StringField(choices=[['a. Eli Whitney', 'a. Eli Whitney'], ['b. Oprah Winfrey', 'b. Oprah Winfrey'], ['c. Thomas Edison', 'c. Thomas Edison'], ['d. Enrico Marconi', 'd. Enrico Marconi']], label='Who is credited with inventing the light bulb?')
    # q15 = models.StringField(choices=[['a. Texas', 'a. Texas'], ['b. Montana', 'b. Montana'], ['c. Maine', 'c. Maine'], ['d. North Carolina', 'd. North Carolina']], label='“First in Flight” is the slogan of which of the following states?')


def calculate_score(player: Player):
    score = 0
    for field_name in C.CORRECT_ANSWERS:
        if getattr(player, field_name) == C.CORRECT_ANSWERS[field_name]:
            score += 1
    player.score = score
    player.payment = c(60) if score >= 8 else c(30)
    player.participant.vars['quiz_payment'] = player.payment


class Results(Page):
    def before_next_page(player: Player, timeout_happened):
        # Calculate the score before moving to the Results page
        calculate_score(player)
        
    def vars_for_template(player: Player):
        # Pass the score and payment to the template
        return dict(
            score=player.score,
            payment=player.payment
        )


def custom_export(players):
    yield ['participant_code', 'id_in_group']
    for p in players:
        pp = p.participant
        yield [pp.code, p.id_in_group]
class Quiz(Page):
    form_model = 'player'
    form_fields = ['q1'
                #    , 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15'
                   ]
    def before_next_page(player: Player, timeout_happened):
        # Calculate the score at the end of the quiz
        calculate_score(player)

page_sequence = [Quiz, Results]