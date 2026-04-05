import random

class Grammar:
    def __init__(self, VN, VT, productions, start_symbol):
        self.VN = VN
        self.VT = VT
        self.productions = productions
        self.start_symbol = start_symbol
    
    def generate_string(self):
        """
        Generate one valid string from the grammar
        """
        # Convert start symbol to a list of characters for easier manipulation
        current = list(self.start_symbol)
        
        # Keep going until no non-terminals remain
        max_iterations = 100  # Safety limit
        for _ in range(max_iterations):
            # Find positions of all non-terminals
            non_terminal_positions = []
            for i, symbol in enumerate(current):
                if symbol in self.VN:
                    non_terminal_positions.append(i)
            
            # If no non-terminals, we're done
            if not non_terminal_positions:
                break
            
            # Pick a random non-terminal to replace
            pos_to_replace = random.choice(non_terminal_positions)
            symbol_to_replace = current[pos_to_replace]
            
            # Choose a random production
            replacement = random.choice(self.productions[symbol_to_replace])
            
            # Replace the symbol with the production
            current.pop(pos_to_replace)
            for j, char in enumerate(replacement):
                current.insert(pos_to_replace + j, char)
        
        # Join the list into a string
        result = ''.join(current)
        
        # Verify no non-terminals remain (if they do, try again recursively)
        for symbol in self.VN:
            if symbol in result:
                return self.generate_string()  # Try again
        
        return result
    
    def to_finite_automaton(self):
        """
        Convert grammar to finite automaton
        """
        from finite_automaton import FiniteAutomaton
        
        # States = VN ∪ {final_state}
        states = set(self.VN)
        final_state = "FINAL"
        states.add(final_state)
        
        # Alphabet = VT
        alphabet = set(self.VT)
        
        # Initial state = start_symbol
        initial_state = self.start_symbol
        
        # Final states = {final_state}
        final_states = {final_state}
        
        # Transition function delta
        delta = {}
        
        # Initialize delta for all states
        for state in states:
            delta[state] = {}
        
        # Convert productions to transitions
        for non_terminal, productions_list in self.productions.items():
            for production in productions_list:
                if len(production) == 1 and production in self.VT:
                    # Production like D → a
                    # This means: from state D, read 'a', go to FINAL
                    delta[non_terminal][production] = final_state
                
                elif len(production) == 2:
                    first_char = production[0]
                    second_char = production[1]
                    
                    if first_char in self.VT and second_char in self.VN:
                        # Production like S → aS
                        # This means: from state S, read 'a', go to state S
                        delta[non_terminal][first_char] = second_char
        
        return FiniteAutomaton(states, alphabet, delta, initial_state, final_states)
