from typing import Dict, Set, Tuple, List
from copy import deepcopy

class FiniteAutomaton:
    def __init__(self, states: Set[str], alphabet: Set[str], transitions: Dict[Tuple[str, str], Set[str]], 
                 start_state: str, final_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
    
    @classmethod
    def from_variant_22(cls):
        """Create the automaton from Variant 22"""
        states = {'q0', 'q1', 'q2'}
        alphabet = {'a', 'b'}
        transitions = {
            ('q0', 'a'): {'q0'},
            ('q1', 'b'): {'q1', 'q2'},
            ('q0', 'b'): {'q1'},
            ('q1', 'a'): {'q0'},
            ('q2', 'b'): {'q1'}
        }
        start_state = 'q0'
        final_states = {'q2'}
        
        return cls(states, alphabet, transitions, start_state, final_states)
    
    def is_deterministic(self) -> bool:
        """Check if the automaton is deterministic"""
        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) > 1:
                return False
            if symbol not in self.alphabet:
                return False
        
        # Check if all transitions are defined
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    return False
        
        return True
    
    def to_regular_grammar(self):
        """Convert FA to regular grammar"""
        from Grammar import Grammar
        
        productions = {}
        
        # For each transition, create a production rule
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                if state not in productions:
                    productions[state] = []
                
                # Add production: state -> symbol next_state
                productions[state].append(f"{symbol}{next_state}")
        
        # Add epsilon productions for final states
        for final_state in self.final_states:
            if final_state not in productions:
                productions[final_state] = []
            productions[final_state].append("ε")
        
        return Grammar(self.states, self.alphabet, productions, self.start_state)
    
    def ndfa_to_dfa(self):
        """Convert NDFA to DFA using subset construction"""
        if self.is_deterministic():
            return self
        
        # Initialize DFA components
        dfa_states = set()
        dfa_transitions = {}
        dfa_start_state = frozenset([self.start_state])
        dfa_final_states = set()
        
        # Queue for processing new DFA states
        unprocessed_states = [dfa_start_state]
        processed_states = set()
        
        while unprocessed_states:
            current_state = unprocessed_states.pop(0)
            
            if current_state in processed_states:
                continue
            
            processed_states.add(current_state)
            dfa_states.add(current_state)
            
            # Check if this DFA state contains any final state
            if any(state in self.final_states for state in current_state):
                dfa_final_states.add(current_state)
            
            # For each symbol in alphabet, compute the next state
            for symbol in self.alphabet:
                next_states = set()
                
                for nfa_state in current_state:
                    # Get transitions for this NFA state and symbol
                    if (nfa_state, symbol) in self.transitions:
                        next_states.update(self.transitions[(nfa_state, symbol)])
                
                if next_states:
                    dfa_next_state = frozenset(next_states)
                    dfa_transitions[(current_state, symbol)] = dfa_next_state
                    
                    if dfa_next_state not in processed_states:
                        unprocessed_states.append(dfa_next_state)
        
        # Convert frozenset states to readable names
        state_mapping = {state: f"S{i}" for i, state in enumerate(sorted(dfa_states, key=lambda x: len(x)))}
        
        # Create a new DFA with readable state names
        renamed_states = set(state_mapping.values())
        renamed_transitions = {}
        
        for (state, symbol), next_state in dfa_transitions.items():
            renamed_transitions[(state_mapping[state], symbol)] = state_mapping[next_state]
        
        renamed_start_state = state_mapping[dfa_start_state]
        renamed_final_states = {state_mapping[state] for state in dfa_final_states}
        
        return FiniteAutomaton(renamed_states, self.alphabet, 
                              {(s, sym): {next_state} for (s, sym), next_state in renamed_transitions.items()},
                              renamed_start_state, renamed_final_states)
    
    def display(self):
        """Display the automaton in a readable format"""
        print(f"States: {self.states}")
        print(f"Alphabet: {self.alphabet}")
        print(f"Start State: {self.start_state}")
        print(f"Final States: {self.final_states}")
        print("Transitions:")
        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) == 1:
                print(f"  δ({state}, {symbol}) = {next_states}")
            else:
                print(f"  δ({state}, {symbol}) = {next_states}")
    
    def generate_dot(self, filename: str = "automaton"):
        """Generate DOT format for visualization"""
        dot = f"digraph {filename} {{\n"
        dot += "  rankdir=LR;\n"
        dot += "  node [shape = circle];\n"
        
        # Mark start state with an incoming arrow
        dot += f"  start [shape = point];\n"
        dot += f"  start -> {self.start_state};\n"
        
        # Mark final states with double circle
        for state in self.final_states:
            dot += f"  {state} [shape = doublecircle];\n"
        
        # Add transitions
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                dot += f"  {state} -> {next_state} [label = \"{symbol}\"];\n"
        
        dot += "}\n"
        
        with open(f"{filename}.dot", "w") as f:
            f.write(dot)
        
        print(f"DOT file generated: {filename}.dot")
        print(f"To visualize, use: dot -Tpng {filename}.dot -o {filename}.png")
