import sys
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

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