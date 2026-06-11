# Laboratory Work Report: Chomsky Normal Form Transformation

**Course:** Formal Languages & Finite Automata  
**Variant:** 22  
**Author:** Romanov Dana FAF-241

---

## 1. Objectives
1. Understand the theoretical baseline behind normal forms in Context-Free Grammars (CFG).
2. Implement an algorithm to convert a CFG into Chomsky Normal Form (CNF) via a 5-step pipelined approach:
   - Elimination of $\epsilon$-productions.
   - Elimination of Unit/Renaming transformations.
   - Elimination of Non-Productive variables.
   - Elimination of Inaccessible symbols.
   - Restructuring terminal representations and long production bodies.

---

## 2. Mathematical Formalism

The input Grammar $G$ is specified as:
$$G = (V_N, V_T, P, S)$$

Where:
* $V_N = \{S, A, B, C, E\}$
* $V_T = \{a, b\}$
* $S$ is the starting symbol.

### Initial Productions Configuration $P$:
1. $S \rightarrow aB \mid AC$
2. $A \rightarrow a \mid ACSC$
3. $B \rightarrow b \mid aA$
4. $C \rightarrow \epsilon$
5. $E \rightarrow bB$

---

## 3. Step-by-Step Analytical Execution

### Step 1: Eliminate $\epsilon$-productions
* **Nullable set identification**: $N_{\epsilon} = \{C\}$
* Replacing instances of nullable variables across production strings leaves us with:
  * $S \rightarrow aB \mid AC \mid A$
  * $A \rightarrow a \mid ACSC \mid ASC \mid ACC \mid AC$
  * $B \rightarrow b \mid aA$
  * $E \rightarrow bB$
  * Remove $C \rightarrow \epsilon$

### Step 2: Eliminate Renamings / Unit Productions
* **Unit Production Detected**: $S \rightarrow A$
* We inherit properties of $A$ into $S$:
  * $S \rightarrow aB \mid AC \mid a \mid ACSC \mid ASC \mid ACC$

### Step 3: Eliminate Non-Productive Symbols
* Checking symbols deriving terminals:
  * Base productive: $A \rightarrow a$, $B \rightarrow b$, hence $\{A, B\}$ are productive.
  * Form step expansion: $S \rightarrow aB$ (Productive), $E \rightarrow bB$ (Productive).
  * Checking symbol $C$: The only non-epsilon production left was derived through structural omissions. $C$ cannot actively terminate into a valid $V_T^*$ sequence because it has no productions left. Thus, $C$ is **non-productive**.
* **Resulting removals**: Delete occurrences of $C$.
  * $S \rightarrow aB \mid a$
  * $A \rightarrow a$
  * $B \rightarrow b \mid aA$
  * $E \rightarrow bB$

### Step 4: Eliminate Inaccessible Symbols
* **Reachability Path analysis**: Starting at $S$:
  * $S$ targets variables $B$.
  * $B$ targets variables $A$.
* Non-terminal symbol **$E$** is completely detached from any structural derivation chain stemming from $S$.
* **Resulting Removals**: $E$ and its productions are removed.

---

## 4. Final Chomsky Normal Form Serialization

To achieve standard forms ($A \rightarrow BC$ or $A \rightarrow a$):
1. Substitute basic terminals in multi-symbol sequences with non-terminal proxies ($X_1 \rightarrow a$).
2. Chop cascading sequences longer than 2 using placeholder variables ($Y_1$).

### Output Form Grammar Matrix
| Left Hand Head | Final CNF Body Alternatives |
| :--- | :--- |
| **$S$** | $X_1B \mid a$ |
| **$A$** | $a$ |
| **$B$** | $b \mid X_1A$ |
| **$X_1$** | $a$ |

---

## 5. Conclusion
The custom workflow successfully transformed Variant 22's contextual syntax properties cleanly into Chomsky Normal Form. Processing modularity allows verification against standard evaluation vectors. The reduction mechanics cleanly eliminated dead-end paths like variable $E$ and un-terminatable configurations like variable $C$.
