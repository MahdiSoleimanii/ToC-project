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

    def is_empty(self):
        if self.start_state in self.accepting_states:
            return False
        else:
            short_strings = []
            for string_length in range(1, len(self.state_set)):
                for generated_string in self.string_generator(string_length):
                    if self.is_accepted(generated_string):
                        short_strings.append(generated_string)
            return short_strings == []
    
    def is_infinite(self):
        long_strings = []
        for string_length in range(len(self.state_set), 2 * len(self.state_set)):
            for generated_string in self.string_generator(string_length):
                if self.is_accepted(generated_string):
                    long_strings = self.string_generator(string_length)
        return not long_strings == []

    def number_of_elements(self):
        if not self.is_infinite():
            elements = []
            for string_length in range(len(self.state_set)):
                for generated_string in self.string_generator(string_length):
                    if self.is_accepted(generated_string):
                        elements.append(generated_string)
            return len(elements)
        else:
            return 'Infinite Language'
        
    def shortest_string(self):
        elements = []
        for string_length in range(len(self.state_set)):
            for generated_string in self.string_generator(string_length):
                if self.is_accepted(generated_string):
                    elements.append(generated_string)
        if elements == []:
            return 'Empty Language'
        elif elements[0] == '':
            return 'The Empty String'
        else:
            return elements[0]
    
    def longest_string(self):
        elements = []
        for string_length in range(len(self.state_set) + 1):
            for generated_string in self.string_generator(string_length):
                if self.is_accepted(generated_string):
                    elements.append(generated_string)

        if elements == []:
            return 'Empty Language'
        elif len(elements[-1]) == len(self.state_set):
            return 'Infinite Language'
        elif elements[-1] == '':
            return 'The Empty String'
        else:
            return elements[-1]
    
    def string_generator(self, length):
        if length == 0:
            return ['']
        else:
            strings = []
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
    
    def union(self, second_dfa):
        union_state_set = []
        for state in self.state_set:
            for other_state in second_dfa.state_set:
                union_state_set.append((state, other_state))

        union_alphabet = self.alphabet

        union_start_state = (self.start_state, second_dfa.start_state)

        union_accepting_states = []
        for accept_state in self.accepting_states:
            for state in second_dfa.state_set:
                if (accept_state, state) not in union_accepting_states:
                    union_accepting_states.append((accept_state, state))
        for accept_state in second_dfa.accepting_states:
            for state in self.state_set:
                if (state, accept_state) not in union_accepting_states:
                    union_accepting_states.append((state, accept_state))

        union_transition_function = {}
        for state in union_state_set:
            union_transition_function[state] = {}
            for char in union_alphabet:
                union_transition_function[state][char] = (self.transition_function[state[0]][char], second_dfa.transition_function[state[1]][char])

        union_dfa = DFA(union_state_set, union_alphabet, union_start_state, union_accepting_states, union_transition_function)

        for state in union_state_set:
            if not union_dfa.is_reachable(state):
                union_dfa.state_set.remove(state)
                union_dfa.accepting_states.remove(state)
                union_dfa.transition_function.pop(state)
        
        return DFA(union_state_set, union_alphabet, union_start_state, union_accepting_states, union_transition_function)
    
    def is_reachable(self, dest_state):
        reachable_states = [self.start_state]
        for state in reachable_states:
            for char in self.alphabet:
                if self.transition_function[state][char] not in reachable_states:
                    reachable_states.append(self.transition_function[state][char])
        return dest_state in reachable_states
                        