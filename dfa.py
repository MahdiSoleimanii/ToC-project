class DFA:
    def __init__(self, state_set, alphabet, start_state, accepting_states, transition_function):
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

    def shortest_string(self):
        shortest_string_length = self.traverse(self.start_state, 0)
        return shortest_string_length

    def traverse(self, current_state, length_counter):
        for char in self.alphabet:
            next_state = self.transition_function[current_state][char]
            if next_state not in self.accepting_states:
                self.traverse(next_state, length_counter + 1)
            else:
                return length_counter