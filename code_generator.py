class CodeGenerator:
    def __init__(self, tokens, lexemas):
        self.tokens = tokens
        self.lexemas = lexemas
        self.pos = 0
        self.codigo_gerado = []
        self.nivel_indentacao = 0

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self):
        print(f"Consumindo token: {self.atual()} lexema: {self.lexemas[self.pos]}")
        self.pos += 1

    def verificar(self, esperado):
        print(f"Verificando: esperado '{esperado}', atual '{self.atual()}'")
        if self.atual() != esperado:
            self.erro(esperado)
        self.consumir()

    def erro(self, esperado):
        encontrado = self.lexemas[self.pos] if self.pos < len(self.lexemas) else 'EOF'
        raise SyntaxError(f"Erro de sintaxe: esperado '{esperado}', encontrado '{encontrado}'.")

    def adicionar_codigo(self, linha):
        indentacao = "    " * self.nivel_indentacao
        self.codigo_gerado.append(f"{indentacao}{linha}")

    def gerar_codigo(self):
        print("Iniciando geração de código.")
        self.programa()
        return '\n'.join(self.codigo_gerado)

    def programa(self):
        print("Início do programa.")
        while self.atual() is not None:
            print(f"Declaração encontrada: {self.atual()}")
            self.declaracao()

    def atribuicao(self):
        print("Iniciando atribuição.")
        var_nome = self.lexemas[self.pos]
        self.verificar('ID')
        
        if self.atual() == 'ATTR':
            self.verificar('ATTR')
            valor = self.expressao()
            self.adicionar_codigo(f"{var_nome} = {valor}")
        
        elif self.atual() == 'CONT':
            self.verificar('CONT')
            self.adicionar_codigo(f"{var_nome} += 1")

    def if_statement(self):
        print("Iniciando estrutura if.")
        self.verificar('IF')
        condicao = self.expressao()
        print(f"Condição do if: {condicao}")
        self.adicionar_codigo(f"if {condicao}:")
        self.nivel_indentacao += 1

        while self.atual() and self.atual() != 'ELSE':
            self.declaracao()
        self.nivel_indentacao -= 1

        if self.atual() == 'ELSE':
            self.consumir()
            self.adicionar_codigo("else:")
            self.nivel_indentacao += 1
            while self.atual():
                self.declaracao()
            self.nivel_indentacao -= 1

    def for_statement(self):
        print("Iniciando estrutura for.")
        self.verificar('FOR')
        var_loop = self.lexemas[self.pos]
        self.verificar('ID')
        self.verificar('IN')
        iteravel = self.expressao()
        self.adicionar_codigo(f"for {var_loop} in {iteravel}:")
        self.nivel_indentacao += 1
        while self.atual() in ('PRINT', 'ID', 'IF', 'WHILE'):
            self.declaracao()
        self.nivel_indentacao -= 1

    def while_statement(self):
        print("Iniciando estrutura while.")
        self.verificar('WHILE')
        condicao = self.expressao()
        self.adicionar_codigo(f"while {condicao}:")
        self.nivel_indentacao += 1
        while self.atual() in ('PRINT', 'ID'):
            self.declaracao()
        self.nivel_indentacao -= 1

    def declaracao(self):
        print(f"Processando declaração para token: {self.atual()}")
        if self.atual() == 'ID':
            self.atribuicao()
        elif self.atual() == 'IF':
            self.if_statement()
        elif self.atual() == 'FOR':
            self.for_statement()
        elif self.atual() == 'WHILE':
            self.while_statement()
        elif self.atual() == 'PRINT':
            self.print_statement()
        elif self.atual() == 'LBRACKET':
            self.lista()
        else:
            self.erro('Declaração')

    def print_statement(self):
        print("Iniciando declaração print.")
        self.verificar('PRINT')
        self.verificar('LPAREN')
        conteudo = []

        while self.atual() in ('ID', 'INTEGER_CONST', 'FLOAT_CONST', 'STRING'):
            conteudo.append(self.lexemas[self.pos])
            self.consumir()
            
            if self.atual() == 'COMMA':
                self.consumir()

        self.verificar('RPAREN')
        self.adicionar_codigo(f"print({', '.join(conteudo)})")

    def termo(self):
        print("Iniciando termo.")
        resultado = self.fator()
        while self.atual() in ('MULT', 'DIV'):
            operador = self.lexemas[self.pos]
            print(f"Operador no termo: {operador}")
            self.consumir()
            resultado += f" {operador} {self.fator()}"
        return resultado

    def expressao(self):
        print("Iniciando expressão.")
        resultado = self.termo()
        while self.atual() in ('PLUS', 'MINUS', 'LT', 'GT', 'EQ', 'NE'):
            operador = self.lexemas[self.pos]
            print(f"Operador na expressão: {operador}")
            self.consumir()
            resultado += f" {operador} {self.termo()}"
        return resultado

    def fator(self):
        if self.atual() == 'INTEGER_CONST':
            valor = self.lexemas[self.pos]
            self.consumir()
            return valor
        elif self.atual() == 'FLOAT_CONST':
            valor = self.lexemas[self.pos]
            self.consumir()
            return valor
        elif self.atual() == 'ID':
            valor = self.lexemas[self.pos]
            self.consumir()
            return valor
        elif self.atual() == 'STRING':
            valor = self.lexemas[self.pos]
            self.consumir()
            return f'"{valor}"'
        elif self.atual() == 'LBRACKET':
            return self.lista()
        elif self.atual() == 'LPAREN':
            self.consumir()
            resultado = self.expressao()
            self.verificar('RPAREN')
            return f"({resultado})"
        else:
            self.erro('Fator')

    def lista(self):
        self.verificar('LBRACKET')
        elementos = []

        if self.atual() != 'RBRACKET':
            elementos.append(self.expressao())

            while self.atual() == 'COMMA':
                self.consumir()
                if self.atual() != 'RBRACKET':
                    elementos.append(self.expressao())
                else:
                    break

        self.verificar('RBRACKET')
        return f"[{', '.join(map(str, elementos))}]" 

