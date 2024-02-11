from otree.api import *
from otree.api import Currency as c
import random

class C(BaseConstants):
    NAME_IN_URL = 'gambling_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 18  # Define the total number of gambling rounds

class Subsession(BaseSubsession):
    @classmethod
    def creating_session(cls):
        for p in cls.get_players():
            # Retrieve initial balance from previous task's earnings or set default
            initial_balance = p.participant.vars.get('quiz_payment', 30)
            # Initialize gamble outcomes for each round
            p.participant.vars['gamble_outcomes'] = []
            for _ in range(C.NUM_ROUNDS):
                orange_balls = random.randint(5, 95)
                white_balls = 100 - orange_balls
                loss_amount = round(random.uniform(0.1, 0.5) * initial_balance, 2)
                insurance_cost = round(random.uniform(0.05, 0.2) * loss_amount, 2)
                # Append gamble outcome for each round
                p.participant.vars['gamble_outcomes'].append({
                    'orange_balls': orange_balls,
                    'white_balls': white_balls,
                    'loss_amount': loss_amount,
                    'insurance_cost': insurance_cost,
                })

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Define player fields for storing decisions and outcomes
    insurance_purchased = models.BooleanField(
        label="Do you want to purchase insurance?",
        widget=widgets.RadioSelect,
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        initial=False
    )
    insurance_cost = models.CurrencyField()
    gamble_number = models.IntegerField()
    orange_balls = models.IntegerField()
    white_balls = models.IntegerField()
    loss_amount = models.CurrencyField()
    ball_drawn = models.StringField()
    round_loss = models.CurrencyField()

class Introduction(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            'intro_text': "In this part of the experiment, you will make decisions about a series of gambles..."
        }


class Gamble(Page):
    form_model = 'player'
    form_fields = ['insurance_purchased']

    @staticmethod
    def is_displayed(player):
        return player.round_number <= C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        # Ensure 'gamble_outcomes' is initialized
        if 'gamble_outcomes' not in player.participant.vars:
            player.participant.vars['gamble_outcomes'] = [{
                'orange_balls': random.randint(5, 95),
                'white_balls': 0,  # This will be calculated based on orange_balls
                'loss_amount': c(0),
                'insurance_cost': c(0),
            } for _ in range(C.NUM_ROUNDS)]

            # Recalculate white_balls based on orange_balls
            for outcome in player.participant.vars['gamble_outcomes']:
                outcome['white_balls'] = 100 - outcome['orange_balls']

        current_round_data = player.participant.vars['gamble_outcomes'][player.round_number - 1]

        return {
            'gamble_number': player.round_number,
            'orange_balls': current_round_data['orange_balls'],
            'white_balls': current_round_data['white_balls'],
            'loss_amount': current_round_data['loss_amount'],
            'insurance_cost': current_round_data['insurance_cost'],
            'initial_earnings': player.participant.vars.get('quiz_payment', c(30)),
            'balance_after_insurance': player.participant.vars.get('quiz_payment', c(30)) - (current_round_data['insurance_cost'] if player.insurance_purchased else c(0)),
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Even if timeout_happened isn't used, it's included to match oTree's expected method signature.
        if timeout_happened:
            # Log or handle timeout scenario if needed
            pass

        current_round_data = player.participant.vars['gamble_outcomes'][player.round_number - 1]
        total_balls = current_round_data['orange_balls'] + current_round_data['white_balls']
        drawn_ball = 'orange' if random.randint(1, total_balls) <= current_round_data['orange_balls'] else 'white'
        
        player.ball_drawn = drawn_ball 

        if drawn_ball == 'orange':
            player.round_loss = current_round_data['insurance_cost'] if player.insurance_purchased else current_round_data['loss_amount']
        else:
            player.round_loss = c(0)

class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.round_number == C.NUM_ROUNDS:
            selected_round = random.randint(1, C.NUM_ROUNDS)
            for player in group.get_players():
                player.participant.vars['selected_round'] = selected_round
                
def apply_selected_round_outcome(player: Player):
    # Apply the outcome of the selected round to determine final payoff
    selected_round = player.participant.vars['selected_round']
    selected_player_in_round = player.in_round(selected_round)
    initial_balance = player.participant.vars.get('quiz_payment', c(30))
    
    if selected_player_in_round.ball_drawn == 'orange' and not selected_player_in_round.insurance_purchased:
        final_balance = initial_balance - selected_player_in_round.loss_amount
    else:
        final_balance = initial_balance - (selected_player_in_round.insurance_cost if selected_player_in_round.insurance_purchased else c(0))
    
    player.payoff = final_balance

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Fallback to round 1 if 'selected_round' wasn't properly set
        # This is a defensive measure and should be logged for further debugging
        selected_round = player.participant.vars.get('selected_round', 1)
        print(f"Selected round for player {player.id_in_group} is {selected_round}")
        
        gamble_outcomes = player.participant.vars.get('gamble_outcomes', [])
        if not gamble_outcomes:  # Safe check if gamble_outcomes wasn't initialized
            print("Error: 'gamble_outcomes' is empty or not set. Please check your session configuration.")
            selected_outcome = {}  # Empty default to prevent further errors in template rendering
        else:
            selected_outcome = gamble_outcomes[selected_round - 1]  # -1 to adjust for list indexing
        
        return {
            'initial_earnings': player.participant.vars.get('quiz_payment', c(30)),
            'selected_round_number': selected_round,
            'orange_balls': selected_outcome.get('orange_balls', 0),
            'white_balls': selected_outcome.get('white_balls', 0),
            'loss_amount': selected_outcome.get('loss_amount', c(0)),
            'insurance_cost': selected_outcome.get('insurance_cost', c(0)),
            'insurance_purchased': selected_outcome.get('insurance_purchased', False),
            'ball_drawn': selected_outcome.get('ball_drawn', 'Not Set'),
            'round_loss': selected_outcome.get('round_loss', c(0)),
            'final_earnings': player.payoff,
        }

page_sequence = [Gamble, ResultsWaitPage, Results]
