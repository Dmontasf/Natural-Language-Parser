# Natural Language to DFA/NFA Parser

This project is a simple parser that interprets basic natural language commands and converts them into their equivalent Deterministic Finite Automaton (DFA) or Nondeterministic Finite Automaton (NFA) representations. It allows users to input structured commands like "turn on the light" or "open the door," which are then tokenized and parsed into formal state machines.

## Features

- Parses simple natural language inputs into finite automata.
- Supports both DFA and NFA generation based on rule definitions.
- Easily extensible with new commands and grammar rules.
- Useful for educational purposes, compilers, or early-stage natural language interfaces.

## Technologies Used

- Python
- Regular Expressions
- Custom grammar/tokenization logic

## Getting Started

1. Clone the repository.
2. Run the parser with Python and input a supported command.
3. View the resulting DFA or NFA structure printed or visualized (if supported).

## Example

Input:
"turn on light"
Output:
States: {q0, q1, q2}
Alphabet: {turn, on, light}
Transitions: ...
Start State: q0
Accept State: q2
