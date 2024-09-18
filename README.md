# C Program Tokenizer

This program is designed to tokenize C program code, separating it into individual tokens or lexemes. Tokenization is a fundamental step in the process of parsing and analyzing C code, as it breaks down the code into its basic building blocks, such as keywords, identifiers, constants, and symbols.

## Features
- **Token Classification**: Classifies tokens into operators, separators, and special symbols.
- **Token Frequency Counting**: Counts the frequency of token types.
- **Dual Display**: Displays both the source code and the corresponding token table in separate windows.
- **Custom Lexer**: Uses a custom lexer module to tokenize C code.

## How It Works

The tokenization process involves scanning through the C code, identifying and categorizing each component, and generating tokens with relevant information such as type, content, and position. These tokens can then be further processed for tasks such as syntax analysis, code generation, or code optimization.

1. **Tokenization**: The input C code is parsed, and tokens are generated.
2. **Classification**: Tokens are classified into operators, separators, and special symbols.
3. **Frequency Analysis**: Token types are counted and displayed in a formatted output.
4. **Display**: The source code and token information are displayed in two separate windows using `tkinter`.

## Usage

To use this program, simply provide it with C program code as input, and it will produce a list of tokens representing the code's lexical structure. The tokenized output can be utilized for various purposes, including compiler development, code analysis, or software testing.

### Code Structure

#### Main Functions

1. **tokenize_code(file)**: Tokenizes the code from the selected file using a custom lexer module.
2. **classify_tokens(toklst, toks_type)**: Classifies the tokens into different categories (operators, separators, etc.).
3. **count_token_frequencies(toks_type)**: Counts the frequencies of each token type.
4. **display_dual_windows(frmt_data, code, toklst)**: Displays the token table and source code in separate windows using `tkinter`.

### Tokenizer Output

- The output includes the tokenized code displayed in two `tkinter` windows: one for the original source code and the other for the tokenized data.
- Token types and frequencies are printed in the console for detailed analysis.

## Requirements

- `python 3.x`
- `tkinter` (for GUI display)
- `tabulate` (for formatting tables)
- `collections.Counter` (for counting token frequencies)

## Screenshots

![1](https://github.com/user-attachments/assets/62e8f611-b330-48e2-93c0-fc74f5ace9ae)
![2](https://github.com/user-attachments/assets/fd7069bd-4c28-4c8f-b4c0-46e192e7e9dc)
![3](https://github.com/user-attachments/assets/12f63e79-d69a-4d1f-bab9-b04886de73cc)
![4](https://github.com/user-attachments/assets/9a7c66ff-7bfa-40b8-9597-8302bb9316ce)
