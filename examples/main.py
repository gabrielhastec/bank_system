from cli.menu import Menu

"""Módulo principal para execução do sistema bancário via CLI.

Define a função main que inicializa e executa a interface de linha de comando.
"""

def main() -> None:
    """Inicia a interface de linha de comando do sistema bancário.

    Cria uma instância da classe Menu e executa seu loop interativo.
    """
    Menu().run()

if __name__ == "__main__":
    main()