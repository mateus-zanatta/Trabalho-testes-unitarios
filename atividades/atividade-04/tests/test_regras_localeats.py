# Responsável: Mateus Zanatta Mariani
# Regra 1: verificar valor mínimo do pedido

import pytest

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


# TU03 (diferencial: caso de borda + parametrize)
@pytest.mark.parametrize(
    ("valor_pedido", "esperado"),
    [
        (29.99, False),  # um centavo abaixo do mínimo
        (30, True),  # exatamente o mínimo
    ],
)
def test_limite_do_valor_minimo_de_30_reais(valor_pedido, esperado):
    resultado = pedido_atingiu_valor_minimo(valor_pedido)

    assert resultado is esperado


# TU04 (diferencial: pytest.raises)
def test_valor_negativo_gera_value_error():
    with pytest.raises(ValueError, match="negativo"):
        pedido_atingiu_valor_minimo(-10)
