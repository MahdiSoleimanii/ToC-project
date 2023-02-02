class DFA:
    def __init__(self, state_set, alphabet, start_state, accepting_states, transition_function):
        self.state_set = state_set
        self.alphabet = alphabet
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function

    def __eq__(self, second_dfa):
        if isinstance(second_dfa, DFA):
            result = True
            for string_length in range(len(self.state_set)):
                for generated_string in self.str_generator(string_length):
                    result = (self.is_accepted(generated_string) == second_dfa.is_accepted(generated_string))
            return result
        else:
            return False
    
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
                for generated_string in self.str_generator(string_length):
                    if self.is_accepted(generated_string):
                        short_strings.append(generated_string)
            return short_strings == []
    
    def is_infinite(self):
        long_strings = []
        for string_length in range(len(self.state_set), 2 * len(self.state_set)):
            for generated_string in self.str_generator(string_length):
                if self.is_accepted(generated_string):
                    long_strings = self.str_generator(string_length)
        return not long_strings == []

    def num_of_elements(self):
        if not self.is_infinite():
            elements = []
            for string_length in range(len(self.state_set)):
                for generated_string in self.str_generator(string_length):
                    if self.is_accepted(generated_string):
                        elements.append(generated_string)
            return len(elements)
        else:
            return 'Infinite Language'
        
    def shortest_str_len(self):
        elements = []
        for string_length in range(len(self.state_set)):
            for generated_string in self.str_generator(string_length):
                if self.is_accepted(generated_string):
                    elements.append(generated_string)
        if elements == []:
            return 'Empty Language'
        else:
            return len(elements[0])
    
    def longest_str_len(self):
        elements = []
        for string_length in range(len(self.state_set) + 1):
            for generated_string in self.str_generator(string_length):
                if self.is_accepted(generated_string):
                    elements.append(generated_string)

        if elements == []:
            return 'Empty Language'
        elif len(elements[-1]) == len(self.state_set):
            return 'Infinite Language'
        else:
            return len(elements[-1])
    
    def str_generator(self, length):
        if length == 0:
            return ['']
        else:
            strings = []
            for string in self.str_generator(length - 1):
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
        union_state_set = self.__q_into_q(second_dfa)

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
        
        return DFA(union_state_set, union_alphabet, union_start_state, union_accepting_states, union_transition_function).del_unreachable()

    def intersection(self, second_dfa):
        intersection_state_set = self.__q_into_q(second_dfa)
        
        intersection_alphabet = self.alphabet

        intersection_start_state = (self.start_state, second_dfa.start_state)

        intersection_accepting_states = []
        for accept_state in self.accepting_states:
            for acc_state in second_dfa.accepting_states:
                intersection_accepting_states.append((accept_state, acc_state))

        intersection_transition_function = {}
        for state in intersection_state_set:
            intersection_transition_function[state] = {}
            for char in intersection_alphabet:
                intersection_transition_function[state][char] = (self.transition_function[state[0]][char], second_dfa.transition_function[state[1]][char])
        
        return DFA(intersection_state_set, intersection_alphabet, intersection_start_state, intersection_accepting_states, intersection_transition_function).del_unreachable()
    
    def difference(self, second_dfa):
        difference_state_set = self.__q_into_q(second_dfa)

        difference_alphabet = self.alphabet

        difference_start_state = (self.start_state, second_dfa.start_state)

        difference_accepting_states = []
        for accept_state in self.accepting_states:
            for state in second_dfa.state_set:
                if state not in second_dfa.accepting_states:
                    difference_accepting_states.append((accept_state, state))

        difference_transition_function = {}
        for state in difference_state_set:
            difference_transition_function[state] = {}
            for char in difference_alphabet:
                difference_transition_function[state][char] = (self.transition_function[state[0]][char], second_dfa.transition_function[state[1]][char])
        
        return DFA(difference_state_set, difference_alphabet, difference_start_state, difference_accepting_states, difference_transition_function).del_unreachable()

    def is_subset_of(self, second_Dfa):
        return self.difference(second_Dfa).is_empty()

    def is_disjoint(self, second_dfa):
        return self.intersection(second_dfa).is_empty()
    
    def __q_into_q(self, second_dfa):
        q_into_q_state_set = []
        for state in self.state_set:
            for other_state in second_dfa.state_set:
                q_into_q_state_set.append((state, other_state))
        
        return q_into_q_state_set
        
    def __reachable_via(self, dest_state):
        reachable_states = [self.start_state]
        for state in reachable_states:
            for char in self.alphabet:
                if self.transition_function[state][char] not in reachable_states:
                    reachable_states.append(self.transition_function[state][char])
        return dest_state in reachable_states
    
    def del_unreachable(self):
        for state in self.state_set:
            if not self.__reachable_via(state):
                self.state_set.remove(state)
                if state in self.accepting_states:
                    self.accepting_states.remove(state)
                self.transition_function.pop(state)
        return self