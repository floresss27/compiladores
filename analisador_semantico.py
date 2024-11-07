from code_generator import Parser
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


class SemanticAnalyzer(Parser):
    def __init__(self, tokens, lexemas):
        super().__init__(tokens, lexemas)
        self.symbol_table = SymbolTable()

    def declaracao_variavel(self):
        tipo = self.atual()
        self.consumir()
        nome = self.lexemas[self.pos]
        self.verificar('ID')
        self.symbol_table.declare(nome, tipo)
        self.verificar('ATTR')
        tipo_valor = self.expressao()
        if tipo != tipo_valor:
            raise ValueError(f"Erro semântico na linha {self.linha_atual}: Tipo incompatível para '{nome}' - esperado '{tipo}', encontrado '{tipo_valor}'")
        self.verificar('PCOMMA')

    def atribuicao(self):
        nome = self.lexemas[self.pos]
        self.verificar('ID')
        tipo_variavel = self.symbol_table.get_type(nome)
        self.verificar('ATTR')
        tipo_valor = self.expressao()
        if tipo_variavel != tipo_valor:
            raise ValueError(f"Erro semântico na linha {self.linha_atual}: Atribuição de tipo incompatível para '{nome}' - esperado '{tipo_variavel}', encontrado '{tipo_valor}'")
        self.verificar('PCOMMA')

    def expressao(self):
        tipo = self.relacional()
        while self.atual() in ('OR', 'AND'):
            self.consumir()
            if tipo != self.relacional():
                raise ValueError(f"Erro semântico na linha {self.linha_atual}: Tipos incompatíveis em operação lógica.")
        return tipo

    def relacional(self):
        tipo = self.termo()
        while self.atual() in ('LT', 'GT', 'LE', 'GE', 'EQ', 'NE'):
            self.consumir()
            tipo_direito = self.termo()

            tipos_compatíveis = (
                (tipo == tipo_direito) or
                (tipo in ('INT', 'INTEGER_CONST') and tipo_direito in ('FLOAT', 'FLOAT_CONST')) or
                (tipo in ('FLOAT', 'FLOAT_CONST') and tipo_direito in ('INT', 'INTEGER_CONST'))
            )
            
            if not tipos_compatíveis:
                raise ValueError(f"Erro semântico na linha {self.linha_atual}: Tipos incompatíveis em operação relacional.")

            if tipo in ('INT', 'INTEGER_CONST') and tipo_direito in ('FLOAT', 'FLOAT_CONST'):
                tipo = 'FLOAT'
            elif tipo in ('FLOAT', 'FLOAT_CONST') and tipo_direito in ('INT', 'INTEGER_CONST'):
                tipo = 'FLOAT'
        
        return tipo

    def termo(self):
        tipo = self.fator()
        while self.atual() in ('MULT', 'DIV', 'PLUS', 'MINUS'):
            self.consumir()
            tipo_direito = self.fator()

            if tipo != tipo_direito and not (
                (tipo in ('INT', 'INTEGER_CONST') and tipo_direito in ('FLOAT', 'FLOAT_CONST')) or
                (tipo in ('FLOAT', 'FLOAT_CONST') and tipo_direito in ('INT', 'INTEGER_CONST'))
            ):
                raise ValueError(f"Erro semântico na linha {self.linha_atual}: Tipos incompatíveis em operação aritmética.")

            if tipo in ('INT', 'INTEGER_CONST') and tipo_direito in ('FLOAT', 'FLOAT_CONST'):
                tipo = 'FLOAT'
            elif tipo in ('FLOAT', 'FLOAT_CONST') and tipo_direito in ('INT', 'INTEGER_CONST'):
                tipo = 'FLOAT'

        return tipo

    def fator(self):
        if self.atual() == 'INTEGER_CONST':
            self.consumir()
            return 'INT'
        elif self.atual() == 'FLOAT_CONST':
            self.consumir()
            return 'FLOAT'
        elif self.atual() == 'ID':
            nome = self.lexemas[self.pos]
            self.consumir()
            return self.symbol_table.get_type(nome)
        elif self.atual() == 'STRING':
            self.consumir()
            return 'STRING'
        elif self.atual() == 'LBRACKET':
            self.verificar('LBRACKET')
            tipo = self.expressao()
            self.verificar('RBRACKET')
            return tipo
        else:
            raise ValueError(f"Erro semântico na linha {self.linha_atual}: Fator inesperado.")
