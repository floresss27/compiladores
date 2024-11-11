class SemanticAnalyzer:
    def __init__(self, tokens, lexemas):
        self.tokens = tokens
        self.lexemas = lexemas
        self.symbol_table = SymbolTable()
        self.pos = 0

    def verificar(self, esperado):
        """Verifica se o token atual é o esperado e consome-o; caso contrário, gera um erro."""
        if self.atual() != esperado:
            raise SyntaxError(f"Erro de sintaxe: esperado '{esperado}', encontrado '{self.atual()}'.")
        self.consumir()

    def consumir(self):
        """Avança para o próximo token."""
        self.pos += 1

    def atual(self):
        """Retorna o token atual."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def analisar(self):
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token == 'ID' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1] == 'ATTR':
                self.verificar_atribuicao()
            elif token == 'PRINT':
                self.verificar_impressao()
            else:
                self.consumir()

    def verificar_atribuicao(self):
        nome_var = self.lexemas[self.pos]
        self.verificar('ID')
        self.verificar('ATTR')
        tipo_valor = self.determinar_tipo() 
        if nome_var not in self.symbol_table.symbols:
            self.symbol_table.declare(nome_var, tipo_valor)
        else:
            tipo_variavel = self.symbol_table.get_type(nome_var)
            if tipo_variavel != tipo_valor:
                raise ValueError(f"Erro semântico: Tipo incompatível para '{nome_var}' - esperado '{tipo_variavel}', encontrado '{tipo_valor}'.")

    def verificar_impressao(self):
        self.verificar('PRINT')
        self.verificar('LPAREN')
        if self.tokens[self.pos] == 'ID':
            nome_var = self.lexemas[self.pos]
            if nome_var not in self.symbol_table.symbols:
                raise ValueError(f"Erro semântico: Variável '{nome_var}' não declarada.")
            self.consumir()
        self.verificar('RPAREN')

    def determinar_tipo(self):
        if self.tokens[self.pos] == 'INTEGER_CONST':
            self.pos += 1
            return 'INT'
        elif self.tokens[self.pos] == 'FLOAT_CONST':
            self.pos += 1
            return 'FLOAT'
        elif self.tokens[self.pos] == 'STRING':
            self.pos += 1
            return 'STRING'
        elif self.tokens[self.pos] == 'ID':
            nome_var = self.lexemas[self.pos]
            self.pos += 1
            if nome_var not in self.symbol_table.symbols:
                raise ValueError(f"Erro semântico: Variável '{nome_var}' não declarada.")
            return self.symbol_table.get_type(nome_var)
        elif self.tokens[self.pos] == 'INPUT':

            self.pos += 1
            if self.tokens[self.pos] == 'LPAREN':
                self.pos += 1
                if self.tokens[self.pos] == 'STRING':
                    self.pos += 1
                self.verificar('RPAREN')
                return 'STRING'
        elif self.tokens[self.pos] == 'INT':

            self.pos += 1
            if self.tokens[self.pos] == 'LPAREN' and self.tokens[self.pos + 1] == 'INPUT':
                self.pos += 1
                self.pos += 1
                if self.tokens[self.pos] == 'LPAREN':
                    self.pos += 1 
                    if self.tokens[self.pos] == 'STRING':
                        self.pos += 1
                    self.verificar('RPAREN')
                self.verificar('RPAREN')
                return 'INT'
        else:
            raise ValueError(f"Erro semântico: Tipo não determinado para o token '{self.tokens[self.pos]}'.")

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, type):
        if name in self.symbols:
            raise ValueError(f"Erro semântico: Variável '{name}' já declarada.")
        self.symbols[name] = type

    def get_type(self, name):
        if name not in self.symbols:
            raise ValueError(f"Erro semântico: Variável '{name}' não declarada.")
        return self.symbols[name]
