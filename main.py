from grammar import Grammar

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
print("=== Generating 5 strings from the grammar ===")
for i in range(5):
    generated = grammar.generate_string()
    print(f"{i+1}. {generated}")
