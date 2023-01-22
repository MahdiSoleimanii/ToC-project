class NFA:
    def __init__(self, state_set, alphabet, start_state, accepting_states, transition_function):
        self.state_set = state_set
        self.alphabet = alphabet
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function

    def del_lambda_tranistion(self):
        pass