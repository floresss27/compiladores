class Parser:
    def __init__(self, tokens, lexemas):
        self.tokens = tokens
        self.lexemas = lexemas
        self.pos = 0

    def atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self):
        self.pos += 1

    def erro(self, esperado):
        raise SyntaxError(f'Erro de sintaxe: esperado {esperado}, encontrado {self.lexemas[self.pos]}')

    def verificar(self, token_esperado):
        if self.atual() == token_esperado:
            self.consumir()
        else:
            self.erro(token_esperado)

    def programa(self):
        while self.pos < len(self.tokens):
            self.declaracao()

    def declaracao(self):
        if self.atual() == 'INT' or self.atual() == 'FLOAT':
            self.declaracao_variavel()
        elif self.atual() == 'ID':
            self.atribuicao()
        elif self.atual() == 'PRINT':
            self.print_statement()
        elif self.atual() == 'IF':
            self.if_statement()
        elif self.atual() == 'FOR':
            self.for_statement()
        else:
            self.erro('Declaração')

    def for_statement(self):
        self.verificar('FOR')
        self.verificar('LBRACKET')
        self.atribuicao()
        self.expressao()
        self.verificar('PCOMMA')
        self.incremento()
        self.verificar('RBRACKET')
        self.verificar('LBRACE')
        while self.atual() != 'RBRACE':
            self.declaracao()
        self.verificar('RBRACE')

    def incremento(self):
        self.verificar('ID')
        self.verificar('ATTR')
        self.verificar('ID')
        self.verificar('PLUS')
        self.verificar('INTEGER_CONST')

    def declaracao_variavel(self):
        self.consumir()
        self.verificar('ID')
        self.verificar('ATTR')
        self.expressao()
        self.verificar('PCOMMA')

    def atribuicao(self):
        self.verificar('ID')
        self.verificar('ATTR')
        self.expressao()
        self.verificar('PCOMMA')

    def if_statement(self):
        self.verificar('IF')
        self.verificar('LBRACKET')
        self.expressao()
        self.verificar('RBRACKET')
        self.bloco()
        if self.atual() == 'ELSE':
            self.consumir()
            self.bloco()

    def while_statement(self):
        self.verificar('WHILE')
        self.verificar('LBRACKET')
        self.expressao()
        self.verificar('RBRACKET') 
        self.bloco()

    def print_statement(self):
        self.verificar('PRINT')
        self.verificar('LBRACKET')
        self.fator()
        self.verificar('RBRACKET')
        self.verificar('PCOMMA')

    def expressao(self):
        self.relacional()
        while self.atual() in ('OR', 'AND'):
            self.consumir()
            self.relacional()

    def relacional(self):
        self.termo()
        while self.atual() in ('LT', 'GT', 'LE', 'GE', 'EQ', 'NE'):
            self.consumir()
            self.termo()

    def termo(self):
        self.fator()
        while self.atual() in ('MULT', 'DIV'):
            self.consumir()
            self.fator()

    def fator(self):
        if self.atual() in ('INTEGER_CONST', 'FLOAT_CONST', 'ID'):
            self.consumir()
        elif self.atual() == 'LBRACKET':
            self.verificar('LBRACKET')
            self.expressao()
            self.verificar('RBRACKET')
        elif self.atual() == 'STRING':
            self.consumir()
        else:
            self.erro('Fator')

    def bloco(self):
        self.verificar('LBRACE')
        while self.atual() != 'RBRACE':
            self.declaracao()
        self.verificar('RBRACE')
