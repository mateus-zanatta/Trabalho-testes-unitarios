# Responsável: Mateus Zanatta Mariani
# Regra 1: verificar valor mínimo do pedido

from src.regras_localeats import pedido_atingiu_valor_minimo


# TU01
def test_pedido_acima_do_minimo_atinge_valor_minimo():
    # Arrange
    valor_pedido = 50

    # Act
    resultado = pedido_atingiu_valor_minimo(valor_pedido)

    # Assert
    assert resultado is True


# TU02
def test_pedido_abaixo_do_minimo_nao_atinge_valor_minimo():
    # Arrange
    valor_pedido = 20

    # Act
    resultado = pedido_atingiu_valor_minimo(valor_pedido)

    # Assert
    assert resultado is False
