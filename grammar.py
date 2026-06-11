class ContextFreeGrammar:
    def __init__(self, vn, vt, productions, start_symbol='S'):
        self.vn = set(vn)
        self.vt = set(vt)
        self.productions = productions  # Dict: {NonTerminal: set(of strings)}
        self.start_symbol = start_symbol

    def print_grammar(self, step_title):
        print(f"\n--- {step_title} ---")
        for head, bodies in sorted(self.productions.items()):
            for body in sorted(bodies):
                print(f"  {head} -> {body if body != '' else 'ε'}")

    def eliminate_epsilon_productions(self):
        """Step 1: Find nullable symbols and eliminate ε-productions."""
        nullable = set()
        
        # Initial nullable detection
        for head, bodies in self.productions.items():
            if '' in bodies:
                nullable.add(head)
                
        # Fixed-point iteration to find all nullable variables
        while True:
            new_nullable = set(nullable)
            for head, bodies in self.productions.items():
                for body in bodies:
                    if body != '' and all(char in nullable for char in body):
                        new_nullable.add(head)
            if new_nullable == nullable:
                break
            nullable = new_nullable

        new_productions = {}
        for head, bodies in self.productions.items():
            new_bodies = set()
            for body in bodies:
                if body != '':
                    # Generate all combinations omitting nullable characters
                    combinations = ['']
                    for char in body:
                        if char in nullable:
                            combinations = [p + c for p in combinations for c in (char, '')]
                        else:
                            combinations = [p + char for p in combinations]
                    for comb in combinations:
                        if comb != '':
                            new_bodies.add(comb)
                elif head == self.start_symbol:
                    # Keep epsilon only if the start symbol itself can derive empty string
                    new_bodies.add('')
            if new_bodies:
                new_productions[head] = new_bodies

        self.productions = new_productions

    def eliminate_renaming(self):
        """Step 2: Eliminate unit productions (renaming) A -> B."""
        unit_pairs = {v: {v} for v in self.vn}
        
        # Build unit pairs using closure
        while True:
            added = False
            for head, bodies in self.productions.items():
                for body in bodies:
                    if len(body) == 1 and body in self.vn:
                        for origin in unit_pairs:
                            if head in unit_pairs[origin] and body not in unit_pairs[origin]:
                                unit_pairs[origin].add(body)
                                added = True
            if not added:
                break

        new_productions = {v: set() for v in self.vn if v in self.productions}
        for head in self.productions:
            for target in unit_pairs.get(head, set()):
                if target in self.productions:
                    for body in self.productions[target]:
                        if not (len(body) == 1 and body in self.vn):
                            if head not in new_productions:
                                new_productions[head] = set()
                            new_productions[head].add(body)
                            
        self.productions = {k: v for k, v in new_productions.items() if v}

    def eliminate_non_productive_symbols(self):
        """Step 4: Keep only symbols that can eventually derive a string of terminals."""
        productive = set()
        
        # Terminals are base-productive elements
        while True:
            new_productive = set(productive)
            for head, bodies in self.productions.items():
                for body in bodies:
                    if all(char in self.vt or char in productive for char in body):
                        new_productive.add(head)
                        break
            if new_productive == productive:
                break
            productive = new_productive

        self.vn = self.vn.intersection(productive)
        new_productions = {}
        for head, bodies in self.productions.items():
            if head in productive:
                valid_bodies = {b for b in bodies if all(c in self.vt or c in productive for c in b)}
                if valid_bodies:
                    new_productions[head] = valid_bodies
        self.productions = new_productions

    def eliminate_inaccessible_symbols(self):
        """Step 3: Keep only symbols reachable from the Start Symbol."""
        accessible = {self.start_symbol}
        queue = [self.start_symbol]
        
        while queue:
            current = queue.pop(0)
            if current in self.productions:
                for body in self.productions[current]:
                    for char in body:
                        if char not in accessible and (char in self.vn or char in self.vt):
                            accessible.add(char)
                            queue.append(char)

        self.vn = self.vn.intersection(accessible)
        self.vt = self.vt.intersection(accessible)
        
        new_productions = {}
        for head, bodies in self.productions.items():
            if head in accessible:
                valid_bodies = {b for b in bodies if all(c in accessible for c in b)}
                if valid_bodies:
                    new_productions[head] = valid_bodies
        self.productions = new_productions

    def to_chomsky_normal_form(self):
        """Step 5: Ensure final syntax matches standard A -> BC or A -> a rules."""
        # Pipeline execution sequence
        self.eliminate_epsilon_productions()
        self.eliminate_renaming()
        self.eliminate_non_productive_symbols()
        self.eliminate_inaccessible_symbols()

        terminal_map = {}
        new_productions = {}
        t_counter = 1
        v_counter = 1

        # Phase A: Handle terminal extraction for mixed or long sequences
        for head, bodies in self.productions.items():
            new_bodies = set()
            for body in bodies:
                if len(body) == 1 and body in self.vt:
                    new_bodies.add(body)
                else:
                    new_body = ""
                    for char in body:
                        if char in self.vt:
                            if char not in terminal_map:
                                terminal_map[char] = f"X{t_counter}"
                                t_counter += 1
                            new_body += terminal_map[char]
                        else:
                            new_body += char
                    new_bodies.add(new_body)
            new_productions[head] = new_bodies

        # Add tracking variables for terminal proxies to VN
        for t_var in terminal_map.values():
            self.vn.add(t_var)
        for term, t_var in terminal_map.items():
            new_productions[t_var] = {term}

        # Phase B: Cascade break downs on lengths > 2
        final_productions = {}
        for head, bodies in new_productions.items():
            final_productions[head] = set()
            for body in bodies:
                # Helper to split variable strings properly
                symbols = []
                i = 0
                while i < len(body):
                    if body[i] in ['X', 'Y']:
                        # Grab symbol tokens like X1, Y12
                        j = i + 1
                        while j < len(body) and body[j].isdigit():
                            j += 1
                        symbols.append(body[i:j])
                        i = j
                    else:
                        symbols.append(body[i])
                        i += 1

                if len(symbols) <= 2:
                    final_productions[head].add("".join(symbols))
                else:
                    current_head = head
                    for k in range(len(symbols) - 2):
                        new_var = f"Y{v_counter}"
                        v_counter += 1
                        self.vn.add(new_var)
                        
                        final_productions[current_head] = final_productions.get(current_head, set())
                        final_productions[current_head].add(symbols[k] + new_var)
                        current_head = new_var
                    
                    final_productions[current_head] = final_productions.get(current_head, set())
                    final_productions[current_head].add(symbols[-2] + symbols[-1])

        self.productions = final_productions
