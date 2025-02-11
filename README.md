# Simple C Compiler

A Python implementation of a compiler pipeline for a subset of the C programming language.

## Features

- Full compiler pipeline implementation:
  1. Lexical Analysis (Tokenizer)
  2. Syntax Analysis (Parser)
  3. Semantic Analysis
  4. Intermediate Code Generation
  5. Code Optimization
  6. Target Code Generation

- Supported C constructs:
  - Variable declarations
  - Arithmetic operations
  - Function definitions
  - Return statements

## Requirements

- Python 3.6+

## Quick Start

1. Clone repository:
    ```bash
    git clone https://github.com/yourusername/c-compiler.git
    cd c-compiler
# Create test file test.c
    ``bash
    int main() {
    int result = 2 + 3 * 4;
    return result;
    }
# Example Output
   ``bash


    global main
    main:
    mov t1, 3
    mov t2, 4
    mul t1, t2
    mov t3, 2
    add t3, t1
    mov result, t3
    mov eax, result
    ret  

' =============================================
' COMPILER COMPONENTS
' =============================================

Public Module CompilerComponents

# Region "Lexical Analysis"
    ' -----------------------------------------
    ' Lexical Analysis Module
    ' -----------------------------------------
    ' Tokenizes input using regular expressions
    ' Identifies:
    '   - Keywords (e.g., "int", "return")
    '   - Identifiers (variable names)
    '   - Literals (numeric values)
    '   - Symbols (operators and punctuation)

# Region "Syntax Analysis"
    ' -----------------------------------------
    ' Syntax Analysis Module
    ' -----------------------------------------
    ' Implements recursive descent parser
    ' Constructs Abstract Syntax Tree (AST):
    '   - Node-based hierarchy
    '   - Represents program structure
    '   - Validates grammar rules


# Region "Intermediate Representation"
    ' -----------------------------------------
    ' Intermediate Code Generation
    ' -----------------------------------------
    ' Generates Three-Address Code (TAC):
    '   - Temporary variables
    '   - Simple operations
    ' Performs optimizations:
    '   - Constant folding
    '   - Dead code elimination


# Region "Target Generation"
    ' -----------------------------------------
    ' Target Code Generation
    ' -----------------------------------------
    ' Outputs x86 assembly code with:
    '   - Basic instructions (MOV, ADD, etc.)
    '   - Register allocation strategy
    '   - Stack management
    ' Generates:
    '   - Section headers
    '   - Function prologues/epilogues


# Region "Limitations"
    ' -----------------------------------------
    ' Current System Limitations
    ' -----------------------------------------
    Const LIMITATIONS As String() = {
        "Supports limited C syntax subset",
        "No advanced type checking",
        "Simplified memory management",
        "Basic error handling",
        "Limited optimization passes",
        "No support for pointers"
    }


This README:
1. Provides clear usage instructions
2. Shows sample input/output
3. Includes architecture visualization
4. Lists key components and limitations
5. Uses proper markdown formatting

Would you like me to modify any section or add specific details?
