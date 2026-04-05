import random

class Grammar:
    def __init__(self, VN, VT, productions, start_symbol):
        """
        Initialize a grammar
        
        Args:
            VN: set of non-terminal symbols (like {'S', 'D', 'F'})
            VT: set of terminal symbols (like {'a', 'b', 'c', 'd'})
            productions: dictionary where key is non-terminal, value is list of productions
            start_symbol: the starting non-terminal (like 'S')
        """
        self.VN = VN
        self.VT = VT
        self.productions = productions
        self.start_symbol = start_symbol
    
    def generate_string(self):
        """
        Generate one valid string from the grammar
        Returns a string consisting only of terminal symbols
        """
        # Start with the start symbol
        current_string = self.start_symbol
        
        # Keep replacing non-terminals until none are left
        while True:
            # Check if we still have any non-terminals
            has_non_terminal = False
            for symbol in self.VN:
                if symbol in current_string:
                    has_non_terminal = True
                    break
            
            # If no non-terminals, we're done
            if not has_non_terminal:
                break
            
            # Find the first non-terminal to replace
            for symbol in self.VN:
                if symbol in current_string:
                    # Choose a random production for this non-terminal
                    possible_replacements = self.productions[symbol]
                    chosen_replacement = random.choice(possible_replacements)
                    
                    # Replace ONLY the FIRST occurrence of this non-terminal
                    current_string = current_string.replace(symbol, chosen_replacement, 1)
                    break  # Break out of the for loop and start checking again
        
        return current_string
    
    def to_finite_automaton(self):
        """
        Convert this grammar to a finite automaton
        """
        # We'll implement this in the next step
        pass
