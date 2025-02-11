import re
from collections import defaultdict

# --------------------------
# 1. Lexical Analysis
# --------------------------

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    keywords = {'int', 'return'}
    tokens = [
        ('KEYWORD', r'\b(int|return)\b'),
        ('IDENT', r'[a-zA-Z_]\w*'),
        ('NUMBER', r'\d+'),
        ('OPERATOR', r'[+\-*/=]'),
        ('SYMBOL', r'[{}();,]'),
        ('SKIP', r'\s+'),
    ]
    
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.tokens))
        
    def tokenize(self):
        tokens = []
        for match in self.regex.finditer(self.code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'SKIP':
                continue
            elif kind == 'KEYWORD':
                tokens.append(Token('KEYWORD', value))
            elif kind == 'IDENT':
                tokens.append(Token('IDENT', value))
            elif kind == 'NUMBER':
                tokens.append(Token('NUMBER', int(value)))
            elif kind == 'OPERATOR':
                tokens.append(Token('OPERATOR', value))
            elif kind == 'SYMBOL':
                tokens.append(Token('SYMBOL', value))
        return tokens + [Token('EOF', '')]

# --------------------------
# 2. Syntax Analysis (Parser)
# --------------------------

class ASTNode:
    pass

class FunctionDecl(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class VarDecl(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ReturnStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.parse_function()
    
    def parse_function(self):
        self.consume('KEYWORD', 'int')
        name = self.consume('IDENT').value
        self.consume('SYMBOL', '(')
        self.consume('SYMBOL', ')')
        self.consume('SYMBOL', '{')
        body = []
        while self.current().value != '}':
            body.append(self.parse_statement())
        self.consume('SYMBOL', '}')
        return FunctionDecl(name, body)
    
    def parse_statement(self):
        if self.current().type == 'KEYWORD' and self.current().value == 'int':
            return self.parse_var_decl()
        elif self.current().type == 'KEYWORD' and self.current().value == 'return':
            return self.parse_return()
        raise SyntaxError("Unexpected token")
    
    def parse_var_decl(self):
        self.consume('KEYWORD', 'int')
        name = self.consume('IDENT').value
        self.consume('OPERATOR', '=')
        value = self.parse_expression()
        self.consume('SYMBOL', ';')
        return VarDecl(name, value)
    
    def parse_return(self):
        self.consume('KEYWORD', 'return')
        expr = self.parse_expression()
        self.consume('SYMBOL', ';')
        return ReturnStmt(expr)
    
    def parse_expression(self):
        node = self.parse_term()
        while self.current().type == 'OPERATOR' and self.current().value in '+-*/':
            op = self.consume('OPERATOR').value
            right = self.parse_term()
            node = BinOp(node, op, right)
        return node
    
    def parse_term(self):
        if self.current().type == 'IDENT':
            return self.consume('IDENT').value
        elif self.current().type == 'NUMBER':
            return self.consume('NUMBER').value
        raise SyntaxError("Unexpected term")
    
    def current(self):
        return self.tokens[self.pos]
    
    def consume(self, type, value=None):
        token = self.tokens[self.pos]
        if token.type != type or (value is not None and token.value != value):
            raise SyntaxError(f"Expected {type} {value}, got {token}")
        self.pos += 1
        return token

# --------------------------
# 3. Semantic Analysis
# --------------------------

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = defaultdict(dict)
    
    def analyze(self):
        self.visit(self.ast)
    
    def visit(self, node):
        if isinstance(node, FunctionDecl):
            self.visit_FunctionDecl(node)
        elif isinstance(node, VarDecl):
            self.visit_VarDecl(node)
        elif isinstance(node, ReturnStmt):
            self.visit_ReturnStmt(node)
    
    def visit_FunctionDecl(self, node):
        for stmt in node.body:
            self.visit(stmt)
    
    def visit_VarDecl(self, node):
        if node.name in self.symbol_table:
            raise NameError(f"Duplicate declaration of {node.name}")
        self.symbol_table[node.name] = 'int'
    
    def visit_ReturnStmt(self, node):
        if isinstance(node.expr, str) and node.expr not in self.symbol_table:
            raise NameError(f"Undefined variable {node.expr}")

# --------------------------
# 4. Intermediate Code Generation
# --------------------------

class TACGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = []
        self.temp_count = 0
    
    def generate(self):
        self.visit(self.ast)
        return self.code
    
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def visit(self, node):
        if isinstance(node, FunctionDecl):
            self.visit_FunctionDecl(node)
        elif isinstance(node, VarDecl):
            self.visit_VarDecl(node)
        elif isinstance(node, ReturnStmt):
            self.visit_ReturnStmt(node)
    
    def visit_FunctionDecl(self, node):
        for stmt in node.body:
            self.visit(stmt)
    
    def visit_VarDecl(self, node):
        value_temp = self.visit_expression(node.value)
        self.code.append(f"{node.name} = {value_temp}")
    
    def visit_ReturnStmt(self, node):
        value_temp = self.visit_expression(node.expr)
        self.code.append(f"RETURN {value_temp}")
    
    def visit_expression(self, node):
        if isinstance(node, BinOp):
            left_temp = self.visit_expression(node.left)
            right_temp = self.visit_expression(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left_temp} {node.op} {right_temp}")
            return temp
        return str(node)

# --------------------------
# 5. Code Optimization
# --------------------------

class Optimizer:
    def __init__(self, tac):
        self.tac = tac
    
    def optimize(self):
        optimized = []
        for line in self.tac:
            if ' = ' in line:
                temp, expr = line.split(' = ')
                if '+' in expr:
                    a, b = expr.split(' + ')
                    if a.isdigit() and b.isdigit():
                        optimized.append(f"{temp} = {int(a) + int(b)}")
                        continue
            optimized.append(line)
        return optimized

# --------------------------
# 6. Target Code Generation
# --------------------------

class CodeGenerator:
    def __init__(self, tac):
        self.tac = tac
        self.registers = ['eax', 'ebx', 'ecx', 'edx']
        self.reg_map = {}
    
    def generate(self):
        asm = ["section .text", "global main", "main:"]
        for line in self.tac:
            if ' = ' in line:
                dest, src = line.split(' = ')
                asm.append(f"mov eax, {src}")
            elif line.startswith('RETURN'):
                asm.append("ret")
        return '\n'.join(asm)

# --------------------------
# Main Pipeline
# --------------------------

def compile_c(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    
    tac_gen = TACGenerator(ast)
    tac = tac_gen.generate()
    
    optimizer = Optimizer(tac)
    optimized_tac = optimizer.optimize()
    
    code_gen = CodeGenerator(optimized_tac)
    asm = code_gen.generate()
    
    return asm

input_code = """
int main() {
    int a = 2 + 3;
    return a;
}
"""

print("Generated Assembly:")
print(compile_c(input_code))