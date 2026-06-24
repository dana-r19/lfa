class FiniteAutomaton:
    def __init__(self, states, alphabet, delta, initial_state, final_states):
        """
        Initialize a finite automaton
        
        Args:
            states: set of all states (e.g., {'S', 'D', 'F', 'FINAL'})
            alphabet: set of input symbols (e.g., {'a', 'b', 'c', 'd'})
            delta: transition function (dict: state -> {symbol: next_state})
            initial_state: starting state (e.g., 'S')
            final_states: set of accepting states (e.g., {'FINAL'})
        """
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.initial_state = initial_state
        self.final_states = final_states
    
    def string_belongs_to_language(self, input_string):
        """
        Check if a string is accepted by this finite automaton
        
        Args:
            input_string: the string to check
            
        Returns:
            True if accepted, False otherwise
        """
        current_state = self.initial_state
        
        # Process each character in the input string
        for char in input_string:
            # Check if character is in alphabet
            if char not in self.alphabet:
                return False
            
            # Check if there's a transition from current state with this character
            if char not in self.delta.get(current_state, {}):
                return False
            
            # Move to the next state
            current_state = self.delta[current_state][char]
        
        # Check if we ended in a final state
        return current_state in self.final_states
