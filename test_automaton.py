import unittest
from src.FiniteAutomaton import FiniteAutomaton

class TestFiniteAutomaton(unittest.TestCase):
    def setUp(self):
        self.fa = FiniteAutomaton.from_variant_22()
    
    def test_initialization(self):
        self.assertEqual(self.fa.states, {'q0', 'q1', 'q2'})
        self.assertEqual(self.fa.alphabet, {'a', 'b'})
        self.assertEqual(self.fa.start_state, 'q0')
        self.assertEqual(self.fa.final_states, {'q2'})
    
    def test_determinism(self):
        # Variant 22 is non-deterministic due to δ(q1,b) = {q1, q2}
        self.assertFalse(self.fa.is_deterministic())
    
    def test_to_regular_grammar(self):
        grammar = self.fa.to_regular_grammar()
        self.assertIsNotNone(grammar)
        self.assertEqual(grammar.start_symbol, 'q0')
    
    def test_ndfa_to_dfa(self):
        dfa = self.fa.ndfa_to_dfa()
        self.assertTrue(dfa.is_deterministic())
        self.assertIn('S0', dfa.states)  # DFA should have renamed states

if __name__ == '__main__':
    unittest.main()
