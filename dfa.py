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
                    result = result and (self.is_accepted(generated_string) == second_dfa.is_accepted(generated_string))
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
        
    def __reachables(self):
        reachable_states = [self.start_state]
        for state in reachable_states:
            for char in self.alphabet:
                if self.transition_function[state][char] not in reachable_states:
                    reachable_states.append(self.transition_function[state][char])
        return reachable_states
    
    def del_unreachable(self):
        for state in self.state_set:
            if state not in self.__reachables():
                self.state_set.remove(state)
                if state in self.accepting_states:
                    self.accepting_states.remove(state)
                self.transition_function.pop(state)
        return self
    
    def minimize(self):
        removed_unreachables = self.del_unreachable()
        return DFA(removed_unreachables.minimized_states(), removed_unreachables.alphabet, removed_unreachables.minimized_start_state(), removed_unreachables.minimized_accepting_states(), removed_unreachables.minimized_transition_function())

    def __find_mixables(self):
        indexes = self.__num_to_state()
        states = self.__state_to_num()
        check_states = []
        for i in range(len(self.state_set)):
            check_states.append([True] * i)
        
        for i in range(1, len(check_states)):
            for j in range(len(check_states[i])):
                if check_states[i][j]:
                    bool1 = indexes[i] in self.accepting_states
                    bool2 = indexes[j] in self.accepting_states
                    if bool1 != bool2:
                        check_states[i][j] = False
        
        check_states_prev = []
        while check_states_prev != check_states:
            check_states_prev = check_states.copy()
            for i in range(1, len(check_states)):
                for j in range(len(check_states[i])):
                    if check_states[i][j]:
                        for char in self.alphabet:
                            state1 = self.transition_function[indexes[i]][char]
                            state2 = self.transition_function[indexes[j]][char]
                            big_index = max(states[state1], states[state2])
                            small_index = min(states[state1], states[state2])
                            if state1 != state2:
                                if not check_states[big_index][small_index]:
                                    check_states[i][j] = False
                                    break
        return check_states

    def minimized_states(self):
        minimized_state_set = []
        states = set()
        for i in range(1, len(self.__find_mixables())):
            for j in range(len(self.__find_mixables()[i])):
                if self.__find_mixables()[i][j]:
                    states.add(self.__num_to_state()[i])
                    states.add(self.__num_to_state()[j])
            minimized_state_set.append(states)
            states = set()
        
        for i in range(len(minimized_state_set) - 1):
            for j in range(i + 1, len(minimized_state_set)):
                if minimized_state_set[i] & minimized_state_set[j]:
                    minimized_state_set[i] = minimized_state_set[i] | minimized_state_set[j]
                    minimized_state_set[j] = set()

        minimized_state_set = [tuple(sorted(list(set))) for set in minimized_state_set if set]

        for state in self.state_set:
            if state not in str(minimized_state_set):
                minimized_state_set.append((state))

        return minimized_state_set

    def minimized_start_state(self):
        new_start_state = self.start_state
        for mixed_state in self.minimized_states():
            if new_start_state in mixed_state:
                new_start_state = mixed_state
                break
        return new_start_state

    def minimized_accepting_states(self):
        minimized_accepting_states = []
        for state in self.minimized_states():
            for accept_state in self.accepting_states:
                if accept_state in state:
                    minimized_accepting_states.append(state)
                    break
        return minimized_accepting_states
    
    def minimized_transition_function(self):
        minimized_transition_function = {}
        for mixed_state in self.minimized_states():
            minimized_transition_function[mixed_state] = {}
        
        for state in self.state_set:
            for mixed_state in self.minimized_states():
                for char in self.alphabet:
                    if state in mixed_state:
                        minimized_transition_function[mixed_state][char] = self.__state_to_mixed_state()[self.transition_function[state][char]]

        return minimized_transition_function
                    
    def __num_to_state(self):
        state_indexes = {}
        index = 0
        for state in self.state_set:
            state_indexes[index] = state
            index += 1
        return state_indexes
    
    def __state_to_num(self):
        state_indexes = {}
        index = 0
        for state in self.state_set:
            state_indexes[state] = index
            index += 1
        return state_indexes
    
    def __state_to_mixed_state(self):
        states_dict = {}
        for state in self.state_set:
            for mixed_state in self.minimized_states():
                if state in mixed_state:
                    states_dict[state] = mixed_state
        return states_dict