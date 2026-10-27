# Registro TDD — `calcular_taxa_entrega`

Cada cenário foi implementado isoladamente, seguindo Red → Green → Refactor.

## Ciclo 1 — Taxa inicial até 3 km

**Comportamento escolhido:** 2 km e pedido de R$ 50,00 → taxa de R$ 5,00.

- **Red:** `test_cobra_taxa_inicial_ate_3_km` falhou com `ImportError`, pois
  `calcular_taxa_entrega` ainda não existia em `src/pedido.py`.
- **Green:** criada a função retornando `5`, o mínimo para o teste passar.
- **Refactor:** nenhum necessário neste ponto. Suíte completa: 5 passed.

## Ciclo 2 — Adicional por km excedente

**Comportamento escolhido:** 4 km e pedido de R$ 50,00 → taxa de R$ 7,00.

- **Red:** `test_cobra_adicional_por_km_excedente` falhou com `assert 5 == 7`,
  pois a função ignorava a distância.
- **Green:** acima de 3 km, retorna `5 + (distancia_km - 3) * 2`.
- **Refactor:** nenhum necessário neste ponto. Suíte completa: 6 passed.

## Ciclo 3 — Entrega gratuita a partir de R$ 100,00

**Comportamento escolhido:** 5 km e pedido de R$ 100,00 → taxa de R$ 0,00.

- **Red:** `test_entrega_gratis_para_pedido_a_partir_de_100` falhou com
  `assert 9 == 0`, pois o valor do pedido era ignorado.
- **Green:** se `total_pedido >= 100`, retorna `0` antes dos demais cálculos.
- **Refactor:** valores fixos (5, 3, 2, 100) extraídos para constantes
  (`TAXA_BASE_ENTREGA`, `DISTANCIA_INCLUIDA_KM`, `TAXA_POR_KM_EXCEDENTE`,
  `TOTAL_ENTREGA_GRATIS`) e os dois ramos de distância unificados com
  `max(distancia_km - DISTANCIA_INCLUIDA_KM, 0)`. Comportamento inalterado.
  Suíte completa: 7 passed.

## Ciclo 4 (desafio opcional) — Distância negativa

**Comportamento escolhido:** distância negativa deve gerar `ValueError`.

- **Red:** `test_rejeita_distancia_negativa` falhou com
  `DID NOT RAISE ValueError`, pois a função aceitava qualquer distância.
- **Green:** adicionada a validação `if distancia_km < 0: raise ValueError(...)`
  no início da função, antes da regra de entrega gratuita, para que a
  distância inválida seja rejeitada em qualquer valor de pedido.
- **Refactor:** nenhum necessário. Suíte completa: 8 passed.
