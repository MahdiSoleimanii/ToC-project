class DFA:
    def __init__(self, state_set, alphabet, start_state, accepting_states, transition_function):
        self.state_set = state_set
        self.alphabet = alphabet
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function
        self.base_strings = []
        for string_length in range(len(self.state_set) * 2):
            self.base_strings += [string for string in self.string_generator(string_length) if self.is_accepted(string)]
    
    def is_accepted(self, input_string):
        current_state = self.start_state
        for char in input_string:
            current_state = self.transition_function[current_state][char]
        return current_state in self.accepting_states

    def is_empty(self):
        return self.base_strings == []
    
    def is_infinite(self):
        result = False
        for string in self.base_strings:
            if len(string) >= len(self.state_set):
                result = True
                break
        return result

    def number_of_elements(self):
        if not self.is_infinite():
            return len(self.base_strings)
        else:
            return 'Infinite Language'
    
    def string_generator(self, length):
        strings = []
        if length == 0:
            strings.append('')
        else:
            for string in self.string_generator(length - 1):
                for char in self.alphabet:
                    strings.append(string + char)
        return strings
                         
    def compliment(self):
        compliment_accepting_states = []
        for state in self.state_set:
            if state not in self.accepting_states:
                compliment_accepting_states.append(state)
        return DFA(self.state_set, self.alphabet, self.start_state, compliment_accepting_states, self.transition_function)