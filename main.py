from dfa import DFA
import json

with open('testcases.json', 'r') as f:
    testcases = json.load(f)

testfa1 = DFA(testcases[0]['states'], testcases[0]['alphabet'], testcases[0]['start_state'], testcases[0]['accepting_states'], testcases[0]['transition_function'])
testfa2 = DFA(testcases[1]['states'], testcases[1]['alphabet'], testcases[1]['start_state'], testcases[1]['accepting_states'], testcases[1]['transition_function'])
testfa3 = DFA(testcases[2]['states'], testcases[2]['alphabet'], testcases[2]['start_state'], testcases[2]['accepting_states'], testcases[2]['transition_function'])
testfa4 = DFA(testcases[3]['states'], testcases[3]['alphabet'], testcases[3]['start_state'], testcases[3]['accepting_states'], testcases[3]['transition_function'])
testfa5 = DFA(testcases[4]['states'], testcases[4]['alphabet'], testcases[4]['start_state'], testcases[4]['accepting_states'], testcases[4]['transition_function'])
testfa6 = DFA(testcases[5]['states'], testcases[5]['alphabet'], testcases[5]['start_state'], testcases[5]['accepting_states'], testcases[5]['transition_function'])
testfa7 = DFA(testcases[6]['states'], testcases[6]['alphabet'], testcases[6]['start_state'], testcases[6]['accepting_states'], testcases[6]['transition_function'])
testfa8 = DFA(testcases[7]['states'], testcases[7]['alphabet'], testcases[7]['start_state'], testcases[7]['accepting_states'], testcases[7]['transition_function'])
testfa9 = DFA(testcases[8]['states'], testcases[8]['alphabet'], testcases[8]['start_state'], testcases[8]['accepting_states'], testcases[8]['transition_function'])
testfa10 = DFA(testcases[9]['states'], testcases[9]['alphabet'], testcases[9]['start_state'], testcases[9]['accepting_states'], testcases[9]['transition_function'])
testfa11 = DFA(testcases[10]['states'], testcases[10]['alphabet'], testcases[10]['start_state'], testcases[10]['accepting_states'], testcases[10]['transition_function'])
testfa12 = DFA(testcases[11]['states'], testcases[11]['alphabet'], testcases[11]['start_state'], testcases[11]['accepting_states'], testcases[11]['transition_function'])
testfa13 = DFA(testcases[12]['states'], testcases[12]['alphabet'], testcases[12]['start_state'], testcases[12]['accepting_states'], testcases[12]['transition_function'])
testfa14 = DFA(testcases[13]['states'], testcases[13]['alphabet'], testcases[13]['start_state'], testcases[13]['accepting_states'], testcases[13]['transition_function'])
testfa15 = DFA(testcases[14]['states'], testcases[14]['alphabet'], testcases[14]['start_state'], testcases[14]['accepting_states'], testcases[14]['transition_function'])

