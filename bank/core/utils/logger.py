"""Configuração de logging para a aplicação bancária.

Este módulo fornece funções para configurar e recuperar loggers que registram
mensagens tanto em arquivo quanto no console, utilizando configurações definidas
no módulo de configurações da aplicação.
"""

import logging
from pathlib import Path
from bank.core.config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """Cria e configura um logger com saída para arquivo e console.

    Args:
        name (str): Nome do logger, geralmente o nome do módulo.

    Returns:
        logging.Logger: Logger configurado com handlers para arquivo e console.
    """
    log_file = settings.LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configuração do logger
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # Evitar log duplicado
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Log em arquivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Log no console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Adiciona handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def get_logger(name: str) -> logging.Logger:
    """Recupera um logger configurado para o nome especificado.

    Args:
        name (str): Nome do logger, geralmente o nome do módulo.

    Returns:
        logging.Logger: Logger configurado para uso.
    """
    return setup_logger(name)
