# Laboratory Work 3: Lexer & Scanner

**Course:** Formal Languages & Finite Automata  
**Author:** Romanov Dana

---

# Objectives

The objectives of this laboratory work are:

- Understand the role of lexical analysis in compilers and interpreters.
- Explore how a lexer (scanner/tokenizer) transforms a stream of characters into meaningful tokens.
- Implement a lexer for a Mini-Math Language that extends the functionality of a basic calculator.

---

# Theoretical Background

Lexical analysis is the first stage of compilation. During this phase, the source code is read character by character and divided into **tokens**, which are meaningful units used by later compilation stages such as parsing and semantic analysis.

Typical token categories include:

- identifiers;
- keywords;
- numeric literals;
- operators;
- punctuation symbols.

A lexer can be implemented using **regular expressions**, which correspond to **deterministic finite automata (DFA)**. This makes lexical analysis both efficient and easy to extend.

---

# Implementation

## Overview

The implemented lexer provides tokenization for a **Mini-Math Language** with features beyond a simple calculator.

Supported elements include:

- integer literals;
- floating-point literals;
- arithmetic operators (`+`, `-`, `*`, `/`, `^`);
- trigonometric functions (`sin`, `cos`, `tan`);
- variable identifiers;
- comparison operators (`==`, `!=`, `<`, `>`);
- assignment operator (`=`);
- parentheses and commas;
- single-line comments (`//`).

Whitespace and comments are ignored while preserving accurate line and column information.

---

# Lexer Architecture

The lexer follows a **regex-based deterministic finite automaton approach**.

Each token is defined through:

- a regular expression;
- a token type;
- an optional value transformer.

All patterns are combined into a single master regular expression using named groups, allowing the source code to be scanned in a single left-to-right pass.

For every match, the lexer:

1. identifies the corresponding token type;
2. transforms the value if necessary;
3. updates line and column positions;
4. emits the resulting token.

Whitespace and comments are skipped automatically.

When the end of the source is reached, an **EOF** token is generated.

---

# Main Components

## Token Class

The `Token` dataclass contains:

- token type;
- token value;
- line number;
- column number.

This information is preserved for later compilation stages and error reporting.

---

## Lexer Class

The lexer maintains:

- the source code;
- current position;
- current line;
- current column.

Token specifications are stored as tuples containing:

- regex pattern;
- token type;
- transformer function.

A keywords dictionary distinguishes built-in functions from ordinary identifiers.

Example:

```
sin → SIN
cos → COS
tan → TAN
```

instead of treating them as variable names.

---

# Core Algorithm

The `get_next_token()` method performs the following steps:

1. Check whether the end of the source has been reached.
2. Match the master regular expression at the current position.
3. If no match exists, generate an `ERROR` token.
4. Update the current position, line, and column.
5. Determine the matched token type.
6. Convert values when necessary.
7. Skip whitespace and comments.
8. Return the generated token.

The `tokenize()` method repeatedly calls `get_next_token()` until an `EOF` or `ERROR` token is encountered, collecting all generated tokens into a list.

---

# Additional Features

Compared to a basic calculator lexer, this implementation supports:

- floating-point numbers;
- power operator (`^`);
- trigonometric functions;
- comparison operators;
- variable identifiers;
- comments;
- automatic numeric conversion;
- line and column tracking.

Variable names may contain:

- letters;
- digits;
- underscores,

but cannot begin with a digit.

---

# Example

## Input

```text
x = 3.14 + sin(45)
```

## Generated Tokens

| Token | Value |
|----------------|---------|
| VARIABLE | `x` |
| ASSIGN | `=` |
| FLOAT | `3.14` |
| PLUS | `+` |
| SIN | `sin` |
| LPAREN | `(` |
| INTEGER | `45` |
| RPAREN | `)` |
| EOF | `None` |

Each token also stores its corresponding line and column position within the source code.

---

# Conclusions

The laboratory successfully demonstrates both the theoretical and practical aspects of lexical analysis.

The implementation confirms that:

- lexical analysis transforms raw source code into structured tokens;
- regular expressions provide an efficient mechanism for token recognition;
- a regex-based lexer is simple to maintain and extend.

The modular design allows new operators, keywords, or literal types to be added by introducing additional token specifications without modifying the core algorithm.

Compared to a basic calculator lexer, the implementation includes support for floating-point numbers, power operations, trigonometric functions, comparison operators, variables, comments, and detailed position tracking, resulting in a flexible and extensible lexical analyzer.

---

# References

1. Aho, Sethi & Ullman – **Compilers: Principles, Techniques, and Tools**.
2. Course materials on regular expressions and deterministic finite automata.
3. Python `re` module documentation.

---

# Repository

https://github.com/dana-r19/lfa/pull/2
