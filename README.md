# Laboratory Work 2: Finite Automata and Grammar Conversion

**Course:** Formal Languages & Finite Automata  
**Author:** Romanov Dana
**Variant:** 22  


---

# Introduction

This laboratory work explores finite automata and their relationship with formal grammars. The implementation focuses on:

- analyzing deterministic and non-deterministic finite automata;
- converting a finite automaton into a regular grammar;
- converting an NDFA into an equivalent DFA using subset construction;
- classifying the resulting grammar according to the Chomsky hierarchy.

---

# Theoretical Background

## Finite Automata

A finite automaton is a mathematical model of computation defined by the 5-tuple:

**(Q, Σ, δ, q₀, F)**

where:

- **Q** – finite set of states;
- **Σ** – input alphabet;
- **δ** – transition function;
- **q₀** – initial state;
- **F** – set of accepting states.

A string is accepted if, after processing all symbols, the automaton reaches a final state.

## Deterministic vs Non-deterministic Finite Automata

### DFA

A deterministic finite automaton has exactly one transition for every combination of state and input symbol.

### NDFA

A non-deterministic finite automaton may:

- have multiple transitions for the same input symbol;
- optionally include ε-transitions.

Although their behavior differs, DFAs and NDFAs recognize exactly the same class of languages.

## Chomsky Hierarchy

Formal grammars are divided into four classes:

| Type | Name | Production Form |
|----------|--------------------|----------------------------|
| Type 0 | Unrestricted | No restrictions |
| Type 1 | Context-Sensitive | αAβ → αγβ |
| Type 2 | Context-Free | A → γ |
| Type 3 | Regular | A → aB or A → a |

Regular grammars are equivalent in expressive power to finite automata.

---

# Implementation

## Variant 22 Specification

### States

```
Q = {q0, q1, q2}
```

### Alphabet

```
Σ = {a, b}
```

### Final States

```
F = {q2}
```

### Transition Function

```
δ(q0, a) = q0
δ(q0, b) = q1

δ(q1, a) = q0
δ(q1, b) = {q1, q2}

δ(q2, b) = q1
```

Because the transition

```
δ(q1, b) = {q1, q2}
```

has two possible destinations, the automaton is **non-deterministic**.

---

## Determinism Verification

The implementation verifies determinism by checking that every state/input pair has exactly one transition.

If:

- multiple transitions exist, or
- a transition is missing,

the automaton is classified as non-deterministic.

---

## Finite Automaton → Regular Grammar

The conversion follows these rules:

```
δ(A, a) = B
```

becomes

```
A → aB
```

For every final state:

```
F → ε
```

is added.

The grammar start symbol is the automaton's initial state.

---

## NDFA → DFA Conversion

The subset construction algorithm is used.

Steps:

1. Start with the set containing the NFA initial state.
2. Compute reachable sets for every input symbol.
3. Create new DFA states when new subsets appear.
4. Mark every subset containing an NFA final state as accepting.
5. Continue until no new subsets are generated.

Generated subsets are renamed to simpler identifiers:

```
S0
S1
S2
```

---

## Chomsky Hierarchy Classification

The classifier analyzes all production rules.

It checks whether productions satisfy:

- **Type 3:** `A → aB` or `A → a`
- **Type 2:** `A → γ`
- **Type 1:** context-sensitive restrictions
- **Type 0:** unrestricted productions

---

# Results

## Determinism Analysis

The automaton is classified as **non-deterministic** because:

```
δ(q1, b) = {q1, q2}
```

contains two possible next states.

All remaining transitions are deterministic.

---

## Regular Grammar

The generated grammar consists of:

### Non-terminals

```
{q0, q1, q2}
```

### Terminals

```
{a, b}
```

### Production Rules

```
q0 → aq0 | bq1

q1 → bq1 | bq2 | aq0

q2 → bq1 | ε
```

The grammar is right-linear since every production follows the form:

```
A → aB
```

or

```
A → a
```

or

```
A → ε
```

---

## Chomsky Classification

The grammar is classified as **Type 3 (Regular Grammar)**.

This result is expected because it was generated directly from a finite automaton, and regular grammars are equivalent to finite automata.

---

## NDFA to DFA Conversion

The subset construction algorithm produced the following DFA:

| DFA State | NFA States |
|------------|----------------|
| S0 | {q0} |
| S1 | {q0, q1} |
| S2 | {q0, q1, q2} |

### DFA Transition Function

```
δ(S0, a) = S0
δ(S0, b) = S1

δ(S1, a) = S0
δ(S1, b) = S2

δ(S2, a) = S0
δ(S2, b) = S2
```

### Final State

```
S2
```

since it contains the NFA final state `q2`.

The resulting automaton is fully deterministic.

---

# Visual Representation

The project generates Graphviz **DOT** files for both the original NDFA and the converted DFA.

They can be rendered with:

```bash
dot -Tpng filename.dot -o filename.png
```

The generated diagrams display:

- states as nodes;
- accepting states as double circles;
- the start state with an incoming arrow;
- labeled transitions between states.

The NDFA visualization highlights the two transitions from `q1` on input `b`, while the DFA contains exactly one transition for every state-symbol pair.

---

# Conclusions

The objectives of this laboratory work were successfully achieved.

The implementation:

- correctly identified the automaton as non-deterministic;
- converted the automaton into an equivalent regular grammar;
- classified the grammar as **Type 3** in the Chomsky hierarchy;
- converted the NDFA into an equivalent DFA using subset construction.

These results demonstrate the equivalence between finite automata and regular grammars while providing practical experience with automata transformations and formal language theory.

---

# Repository

https://github.com/dana-r19/lfa/pull/1
