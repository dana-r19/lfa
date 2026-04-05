from grammar import Grammar
from finite_automaton import FiniteAutomaton

def main():
    # Define your grammar (Variant 22)
    VN = {'S', 'D', 'F'}
    VT = {'a', 'b', 'c', 'd'}
    
    productions = {
        'S': ['aS', 'bS', 'cD'],
        'D': ['dD', 'bF', 'a'],
        'F': ['bS', 'a']
    }
    
    start_symbol = 'S'
    
    # Create the grammar
    grammar = Grammar(VN, VT, productions, start_symbol)
    
    # Generate 5 strings
    print("=" * 50)
    print("PART 1: Generating 5 valid strings from the grammar")
    print("=" * 50)
    
    generated_strings = []
    for i in range(5):
        generated = grammar.generate_string()
        generated_strings.append(generated)
        print(f"{i+1}. {generated}")
    
    # Convert grammar to finite automaton
    print("\n" + "=" * 50)
    print("PART 2: Converting Grammar to Finite Automaton")
    print("=" * 50)
    
    automaton = grammar.to_finite_automaton()
    print("Conversion completed successfully!")
    print(f"States: {automaton.states}")
    print(f"Alphabet: {automaton.alphabet}")
    print(f"Initial state: {automaton.initial_state}")
    print(f"Final states: {automaton.final_states}")
    print("Transitions:")
    for state, transitions in automaton.delta.items():
        for symbol, next_state in transitions.items():
            print(f"  δ({state}, {symbol}) = {next_state}")
    
    # Test strings with the finite automaton
    print("\n" + "=" * 50)
    print("PART 3: Testing strings with the Finite Automaton")
    print("=" * 50)
    
    test_strings = [
        "cda",      # Should be accepted (S→cD, D→dD, D→a)
        "cdaa",     # Should be accepted (S→cD, D→dD, D→a? wait, that gives "cda" not "cdaa")
        "cda",      # Let's test properly
        "cdaa",     # Let's see
        "aa",       # Should be rejected
        "cdaaa",    # Let's test
        "cbSa",     # Contains S - should be rejected
        "cdba",     # Should be accepted? Let's check
    ]
    
    # Also test the generated strings
    print("\n--- Testing generated strings ---")
    for test_str in generated_strings:
        result = automaton.string_belongs_to_language(test_str)
        print(f"'{test_str}': {'ACCEPTED' if result else 'REJECTED'}")
    
    print("\n--- Testing custom strings ---")
    for test_str in test_strings:
        result = automaton.string_belongs_to_language(test_str)
        print(f"'{test_str}': {'ACCEPTED' if result else 'REJECTED'}")

if __name__ == "__main__":
    main()
