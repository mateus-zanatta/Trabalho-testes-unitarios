"""Regras de negocio relacionadas ao calculo de pedidos."""


def validar_item(item: dict) -> None:
    """Valida preco e quantidade de um item.

    Raises:
        ValueError: se o preco ou a quantidade nao forem positivos.
    """
    if item["preco"] <= 0:
        raise ValueError("O preco deve ser positivo.")

    if item["quantidade"] <= 0:
        raise ValueError("A quantidade deve ser positiva.")


def calcular_total(itens: list[dict]) -> float:
    """Calcula o total do pedido.

    Uma lista vazia resulta em total igual a zero.
    """
    total = 0

    for item in itens:
        validar_item(item)
        total += item["preco"] * item["quantidade"]

    return total


TAXA_BASE_ENTREGA = 5
DISTANCIA_INCLUIDA_KM = 3
TAXA_POR_KM_EXCEDENTE = 2
TOTAL_ENTREGA_GRATIS = 100


def calcular_taxa_entrega(distancia_km, total_pedido):
    """Calcula a taxa de entrega.

    Regras:
    - ate 3 km, a taxa e R$ 5;
    - acima de 3 km, acrescenta R$ 2 por quilometro excedente;
    - pedidos a partir de R$ 100 possuem entrega gratuita.

    Raises:
        ValueError: se a distancia for negativa.
    """
    if distancia_km < 0:
        raise ValueError("A distancia nao pode ser negativa.")

    if total_pedido >= TOTAL_ENTREGA_GRATIS:
        return 0

    km_excedente = max(distancia_km - DISTANCIA_INCLUIDA_KM, 0)

    return TAXA_BASE_ENTREGA + km_excedente * TAXA_POR_KM_EXCEDENTE
