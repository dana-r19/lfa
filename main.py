from FiniteAutomaton import FiniteAutomaton

def main():
    print("=" * 60)
    print("Finite Automaton - Variant 22")
    print("=" * 60)
    
    # Create the automaton from variant 22
    fa = FiniteAutomaton.from_variant_22()
    
    print("\n1. Original Finite Automaton:")
    print("-" * 40)
    fa.display()
    
    # Check determinism
    print("\n2. Determinism Check:")
    print("-" * 40)
    is_det = fa.is_deterministic()
    print(f"The automaton is {'deterministic' if is_det else 'non-deterministic'}")
    
    # Convert to regular grammar
    print("\n3. Conversion to Regular Grammar:")
    print("-" * 40)
    grammar = fa.to_regular_grammar()
    grammar.display()
    
    # Classify grammar
    print("\n4. Chomsky Hierarchy Classification:")
    print("-" * 40)
    classification = grammar.classify_chomsky()
    print(f"Grammar Classification: {classification}")
    
    # Convert NDFA to DFA
    if not is_det:
        print("\n5. Converting NDFA to DFA:")
        print("-" * 40)
        dfa = fa.ndfa_to_dfa()
        print("DFA after conversion:")
        dfa.display()
        
        # Verify DFA is deterministic
        print(f"\nIs the converted automaton deterministic? {dfa.is_deterministic()}")
    else:
        print("\n5. NDFA to DFA Conversion:")
        print("-" * 40)
        print("Automaton is already deterministic, no conversion needed")
    
    # Generate DOT files for visualization
    print("\n6. Generating Visualization Files:")
    print("-" * 40)
    fa.generate_dot("ndfa_variant22")
    if not is_det:
        dfa.generate_dot("dfa_variant22")
    
    print("\n" + "=" * 60)
    print("Implementation completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
