
# bank/exceptions.py

class BancoError(Exception):
    """Classe base para exceções do sistema bancário."""
    pass

class SaldoInsuficienteError(BancoError):
    """Exceção levantada quando não há saldo suficiente para o saque."""
    pass

class LimiteSaquesExcedidoError(BancoError):
    """Exceção levantada quando o número máximo de saques é excedido."""
    pass

class ValorInvalidoError(BancoError):
    """Exceção levantada quando o valor informado é inválido (negativo ou zero)."""
    pass
