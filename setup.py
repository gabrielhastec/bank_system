from setuptools import setup, find_packages

"""
Arquivo de configuração do pacote Python para o sistema bancário.

Define os metadados e a estrutura do pacote bank_system, incluindo nome, versão,
descrição e pacotes a serem incluídos, para distribuição e instalação.
"""

setup(
    name="bank_system",
    version="0.1.0",
    description="Mini framework bancário modular",
    packages=find_packages(exclude=("tests", "examples", "migrations")),
    include_package_data=True,
    install_requires=[],
)
