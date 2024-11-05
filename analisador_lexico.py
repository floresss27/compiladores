import re

class AnalisadorLexico:
    linha_atual = 1

    def analisar(self, codigo):
        regras = [
            ('MAIN', r'main'),
            ('INT', r'int'),
            ('FLOAT', r'float'),
            ('IF', r'if'),
            ('ELSE', r'else'),
            ('WHILE', r'while'),
            ('FOR', r'for'),
            ('READ', r'read'),
            ('PRINT', r'print'),
            ('LBRACKET', r'\('),
            ('RBRACKET', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('COMMA', r','),
            ('PCOMMA', r';'),
            ('EQ', r'=='),
            ('NE', r'!='),
            ('LE', r'<='),
            ('GE', r'>='),
            ('OR', r'\|\|'),
            ('AND', r'&&'),
            ('ATTR', r'\='),
            ('LT', r'<'),
            ('GT', r'>'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULT', r'\*'),
            ('DIV', r'\/'),
            ('ID', r'[a-zA-Z]\w*'),
            ('FLOAT_CONST', r'\d+\.\d+'),
            ('INTEGER_CONST', r'\d+'),
            ('STRING', r'"[^"]*"'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]

        tokens_regex = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in regras)
        inicio_linha = 0

        tokens, lexemas, linhas, colunas = [], [], [], []

        for m in re.finditer(tokens_regex, codigo):
            tipo_token = m.lastgroup
            valor_token = m.group(tipo_token)

            if tipo_token == 'NEWLINE':
                inicio_linha = m.end()
                self.linha_atual += 1
            elif tipo_token == 'SKIP':
                continue
            elif tipo_token == 'MISMATCH':
                raise RuntimeError(f'{valor_token!r} inesperado na linha {self.linha_atual}')
            else:
                col = m.start() - inicio_linha
                colunas.append(col)
                tokens.append(tipo_token)
                lexemas.append(valor_token)
                linhas.append(self.linha_atual)
                print(f'Token = {tipo_token}, Lexema = \'{valor_token}\', Linha = {self.linha_atual}, Coluna = {col}')

        return tokens, lexemas, linhas, colunas
