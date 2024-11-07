class AnalisadorLexico:
    def __init__(self):
        self.tokens = []
        self.linha_atual = 1
        self.coluna_atual = 0

    def analisar(self, codigo):
        i = 0
        while i < len(codigo):
            char = codigo[i]
            if char in ' \t':
                self.coluna_atual += 1
                i += 1
                continue
            elif char == '\n':
                self.linha_atual += 1
                self.coluna_atual = 0
                i += 1
                continue

            if char.isalpha() or char == '_':
                inicio = i
                while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                    i += 1
                lexema = codigo[inicio:i]
                tipo_token = self.verificar_palavra_reservada(lexema)
                self.tokens.append((tipo_token, lexema, self.linha_atual, self.coluna_atual))
                self.coluna_atual += i - inicio

            elif char.isdigit():
                inicio = i
                while i < len(codigo) and codigo[i].isdigit():
                    i += 1
                # Verifica se é um número decimal
                if i < len(codigo) and codigo[i] == '.':
                    i += 1
                    while i < len(codigo) and codigo[i].isdigit():
                        i += 1
                    tipo_token = 'FLOAT_CONST'
                else:
                    tipo_token = 'INTEGER_CONST'
                lexema = codigo[inicio:i]
                self.tokens.append((tipo_token, lexema, self.linha_atual, self.coluna_atual))
                self.coluna_atual += len(lexema)
                continue

            elif char in '+-*/<>=!':
                if char == '=' and i + 1 < len(codigo) and codigo[i + 1] == '=':
                    self.tokens.append(('EQ', '==', self.linha_atual, self.coluna_atual))
                    i += 2
                elif char == '!' and i + 1 < len(codigo) and codigo[i + 1] == '=':
                    self.tokens.append(('NE', '!=', self.linha_atual, self.coluna_atual))
                    i += 2
                else:
                    self.tokens.append((self.verificar_operador(char), char, self.linha_atual, self.coluna_atual))
                    i += 1
                self.coluna_atual += 1

            elif char in '{}[],;:()':
                self.tokens.append((self.verificar_delimitador(char), char, self.linha_atual, self.coluna_atual))
                self.coluna_atual += 1
                i += 1

            elif char == '"':
                inicio = i
                i += 1
                while i < len(codigo) and codigo[i] != '"':
                    i += 1
                if i >= len(codigo):
                    raise RuntimeError(f'String não finalizada na linha {self.linha_atual}')
                lexema = codigo[inicio:i + 1]
                self.tokens.append(('STRING', lexema, self.linha_atual, self.coluna_atual))
                self.coluna_atual += i - inicio + 1
                i += 1

            else:
                raise RuntimeError(f'Caractere inesperado {char!r} na linha {self.linha_atual}, coluna {self.coluna_atual}')
            i += 1

        tipos_tokens, lexemas, linhas, colunas = zip(*self.tokens)
        return list(tipos_tokens), list(lexemas), list(linhas), list(colunas)

    def verificar_palavra_reservada(self, lexema):
        palavras_reservadas = {
            'main': 'MAIN', 'class': 'CLASS', 'def': 'DEF', 'int': 'INT',
            'float': 'FLOAT', 'string': 'STRING', 'if': 'IF', 'else': 'ELSE',
            'while': 'WHILE', 'for': 'FOR', 'read': 'READ', 'print': 'PRINT', 'in': 'IN'
        }
        return palavras_reservadas.get(lexema, 'ID')

    def verificar_operador(self, char):
        operadores = {
            '+': 'PLUS', '-': 'MINUS', '*': 'MULT', '/': 'DIV',
            '<': 'LT', '>': 'GT', '=': 'ATTR',
        }
        return operadores.get(char, 'UNKNOWN')

    def verificar_delimitador(self, char):
        delimitadores = {
            '{': 'LBRACE', '}': 'RBRACE', '[': 'LBRACKET', ']': 'RBRACKET',
            ',': 'COMMA', ';': 'PCOMMA', ':': 'COLON', '(': 'LPAREN', ')': 'RPAREN'
        }
        return delimitadores.get(char, 'UNKNOWN')
