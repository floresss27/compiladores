from analisador_lexico import AnalisadorLexico
from analisador_sintatico import Parser
from analisador_semantico import SemanticAnalyzer
from code_generator import CodeGenerator

if __name__ == "__main__":
    with open("code.txt", "r") as file:
        codigo_exemplo = file.read()

    analisador_lexico = AnalisadorLexico()
    tokens, lexemas, linhas, colunas = analisador_lexico.analisar(codigo_exemplo)

    print("\nTokens e Lexemas gerados pelo Analisador Léxico:")
    for i in range(len(tokens)):
        print(f"Token: {tokens[i]}, Lexema: '{lexemas[i]}', Linha: {linhas[i]}, Coluna: {colunas[i]}")

    parser = Parser(tokens, lexemas)
    parser.programa()
    print("\nAnálise sintática concluída com sucesso!")

    analyzer = SemanticAnalyzer(tokens, lexemas)
    analyzer.programa()
    print("\nAnálise semântica concluída com sucesso!")

    generator = CodeGenerator(tokens, lexemas)
    codigo_gerado = generator.gerar_codigo()
    print("\nCódigo Gerado:")
    print(codigo_gerado)
