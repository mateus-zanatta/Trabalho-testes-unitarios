"""Regras de negocio do LocalEats."""

VALOR_MINIMO_PEDIDO = 30


def pedido_atingiu_valor_minimo(valor_pedido):
    """Indica se o pedido atingiu o valor minimo de R$ 30,00.

    Regras:
    - pedidos de R$ 30,00 ou mais retornam True;
    - pedidos abaixo de R$ 30,00 retornam False.

    Raises:
        ValueError: se o valor do pedido for negativo.
    """
    if valor_pedido < 0:
        raise ValueError("O valor do pedido nao pode ser negativo.")

    return valor_pedido >= VALOR_MINIMO_PEDIDO
