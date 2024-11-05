from analisador_semantico import SemanticAnalyzer

class CodeGenerator(SemanticAnalyzer):
    def __init__(self, tokens, lexemas):
        super().__init__(tokens, lexemas)
        self.codigo_gerado = []

    def gerar_codigo(self):
        self.programa()
        return ''.join(self.codigo_gerado)

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
        elif self.atual() == 'FOR':
            self.for_statement()
        elif self.atual() == 'IF':
            self.if_statement()
        else:
            self.erro('Declaração')

    def declaracao_variavel(self):
        tipo = self.atual()
        self.consumir()
        nome = self.lexemas[self.pos]
        self.verificar('ID')
        self.symbol_table.declare(nome, tipo)
        self.verificar('ATTR')
        valor = self.lexemas[self.pos]
        self.expressao()
        self.verificar('PCOMMA')
        self.codigo_gerado.append(f"{tipo.lower()} {nome} = {valor};\n")

    def atribuicao(self):
        nome = self.lexemas[self.pos]
        self.verificar('ID')
        self.verificar('ATTR')
        valor = self.lexemas[self.pos]
        self.expressao()
        self.verificar('PCOMMA')
        self.codigo_gerado.append(f"{nome} = {valor};\n")

    def print_statement(self):
        self.verificar('PRINT')
        self.verificar('LBRACKET')
        mensagem = self.lexemas[self.pos]
        self.fator()
        self.verificar('RBRACKET')
        self.verificar('PCOMMA')
        self.codigo_gerado.append(f"print({mensagem});\n")

    def for_statement(self):
        self.verificar('FOR')
        self.verificar('LBRACKET')

        inicializacao_nome = self.lexemas[self.pos]
        inicializacao_valor = self.lexemas[self.pos + 2]
        if inicializacao_nome not in self.symbol_table.symbols:
            self.symbol_table.declare(inicializacao_nome, 'INT')
        self.atribuicao()

        condicao_variavel = self.lexemas[self.pos]
        operador_condicional = self.lexemas[self.pos + 1]
        valor_condicao = self.lexemas[self.pos + 2]
        self.verificar('ID')
        self.verificar(operador_condicional)
        self.verificar('INTEGER_CONST')
        self.verificar('PCOMMA')

        incremento_variavel = self.lexemas[self.pos]
        self.verificar('ID')
        self.verificar('ATTR')
        self.verificar('ID')
        self.verificar('PLUS')
        incremento_valor = self.lexemas[self.pos + 2]
        self.consumir()

        self.verificar('RBRACKET')
        self.verificar('LBRACE')

        self.codigo_gerado.append(f"{inicializacao_nome} = {inicializacao_valor}\n")
        self.codigo_gerado.append(f"while {condicao_variavel} {operador_condicional} {valor_condicao}:\n")

        while self.atual() != 'RBRACE':
            self.declaracao()
            self.codigo_gerado[-1] = f"    {self.codigo_gerado[-1]}" 
        self.codigo_gerado.append(f"    {incremento_variavel} += {incremento_valor}\n")

        self.verificar('RBRACE')