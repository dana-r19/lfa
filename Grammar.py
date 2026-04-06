from typing import Set, Dict, List

class Grammar:
    def __init__(self, non_terminals: Set[str], terminals: Set[str], 
                 productions: Dict[str, List[str]], start_symbol: str):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
    
    def classify_chomsky(self) -> str:
        """Classify grammar based on Chomsky hierarchy"""
        # Check for Type 0 (Unrestricted) - always true for any grammar
        # Type 1 (Context-Sensitive): αAβ → αγβ where |γ| >= 1, A ∈ Non-terminal
        # Type 2 (Context-Free): A → γ, A ∈ Non-terminal
        # Type 3 (Regular): A → aB or A → a (right-linear) or A → Ba or A → a (left-linear)
        
        is_right_linear = True
        is_left_linear = True
        is_context_free = True
        
        for lhs, rhs_list in self.productions.items():
            # Check if LHS is a single non-terminal (required for Type 2 and 3)
            if len(lhs) != 1 or lhs not in self.non_terminals:
                is_context_free = False
                is_right_linear = False
                is_left_linear = False
                continue
            
            for rhs in rhs_list:
                if rhs == "ε":
                    # Epsilon productions are allowed in Type 2 and 3
                    continue
                
                # Check for right-linear: A → aB or A → a
                if is_right_linear:
                    if len(rhs) == 1:
                        if rhs not in self.terminals and rhs not in self.non_terminals:
                            is_right_linear = False
                    elif len(rhs) == 2:
                        if rhs[0] not in self.terminals or rhs[1] not in self.non_terminals:
                            is_right_linear = False
                    else:
                        is_right_linear = False
                
                # Check for left-linear: A → Ba or A → a
                if is_left_linear:
                    if len(rhs) == 1:
                        if rhs not in self.terminals and rhs not in self.non_terminals:
                            is_left_linear = False
                    elif len(rhs) == 2:
                        if rhs[0] not in self.non_terminals or rhs[1] not in self.terminals:
                            is_left_linear = False
                    else:
                        is_left_linear = False
                
                # Check context-free condition
                if is_context_free:
                    # Already checked LHS is a single non-terminal
                    pass
        
        if is_right_linear or is_left_linear:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        else:
            # Check if context-sensitive (Type 1)
            # For simplicity, if not regular or context-free, assume context-sensitive
            return "Type 1 (Context-Sensitive Grammar) or Type 0 (Unrestricted)"
    
    def display(self):
        """Display grammar in readable format"""
        print(f"Non-terminals: {self.non_terminals}")
        print(f"Terminals: {self.terminals}")
        print(f"Start Symbol: {self.start_symbol}")
        print("Productions:")
        for lhs, rhs_list in self.productions.items():
            print(f"  {lhs} -> {' | '.join(rhs_list)}")
