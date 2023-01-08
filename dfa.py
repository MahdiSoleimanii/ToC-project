class DFA:
    def __init(self, state_set, alphabet, start_state, accepting_states, transition_function):
        self.state_set = state_set
        self.alphabet = alphabet
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function
    
    def is_accepted(self, input_string):
        current_state = self.start_state
        for char in input_string:
            current_state = self.transition_function[current_state][char]
        return current_state in self.accepting_states