"""
Módulo para gerenciamento de migrações do banco de dados.

Define uma função para aplicar migrações incrementais, iniciando com a criação
das tabelas do esquema via create_tables. Novas funções de migração podem ser
adicionadas para atualizar o schema incrementalmente.
"""

from bank.core.schema import create_tables

def migrate() -> None:
    """Aplica migrações incrementais ao banco de dados.

    Atualmente, executa a criação das tabelas do esquema via create_tables.
    Exibe uma mensagem de confirmação após a aplicação.

    Note:
        Novas migrações podem ser adicionadas como funções adicionais neste módulo.
    """
    create_tables()
    print("Migrações aplicadas.")