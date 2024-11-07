from analisador_lexico import AnalisadorLexico
from code_generator import CodeGenerator

if __name__ == "__main__":
    try:
        with open("code.txt", "r") as file:
            codigo_exemplo = file.read()

        analisador_lexico = AnalisadorLexico()
        tokens, lexemas, linhas, colunas = analisador_lexico.analisar(codigo_exemplo)

        print("\nTokens e Lexemas gerados pelo Analisador Léxico:")
        for i in range(len(tokens)):
            print(f"Token: {tokens[i]}, Lexema: '{lexemas[i]}', Linha: {linhas[i]}, Coluna: {colunas[i]}")

        generator = CodeGenerator(tokens, lexemas)
        codigo_gerado = generator.gerar_codigo()

        print("\nCódigo Gerado:")
        print(codigo_gerado)

        with open("codigo_gerado.py", "w") as output_file:
            output_file.write(codigo_gerado)
            print("\nCódigo gerado salvo em 'codigo_gerado.py'")

    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")
    except ValueError as e:
        print(f"Erro semântico: {e}")
    except FileNotFoundError:
        print("Erro: Arquivo 'code.txt' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
