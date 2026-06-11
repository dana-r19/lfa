from grammar import ContextFreeGrammar

if __name__ == "__main__":
    # Context-Free Grammar parsed directly from Variant 22
    V_N = {'S', 'A', 'B', 'C', 'E'}
    V_T = {'a', 'b'}
    
    productions = {
        'S': {'aB', 'AC'},
        'A': {'a', 'ACSC'},
        'B': {'b', 'aA'},
        'C': {''},  # Epsilon production represented as an empty string
        'E': {'bB'}
    }

    print("=== Initializing Processing Engine for Variant 22 ===")
    cfg = ContextFreeGrammar(V_N, V_T, productions, start_symbol='S')
    cfg.print_grammar("Initial Grammar")

    # Step 1
    cfg.eliminate_epsilon_productions()
    cfg.print_grammar("After Eliminating Epsilon (ε) Productions")

    # Step 2
    cfg.eliminate_renaming()
    cfg.print_grammar("After Eliminating Unit Renamings")

    # Step 4
    cfg.eliminate_non_productive_symbols()
    cfg.print_grammar("After Eliminating Non-Productive Symbols")

    # Step 3
    cfg.eliminate_inaccessible_symbols()
    cfg.print_grammar("After Eliminating Inaccessible Symbols")

    # Step 5
    cfg.to_chomsky_normal_form()
    cfg.print_grammar("Final Chomsky Normal Form (CNF)")
    
    print("\nFinal Non-Terminals (V_N):", cfg.vn)
    print("Final Terminals (V_T):", cfg.vt)
