# Aula 11 — Testes unitários e TDD

Prática de testes unitários com Python e pytest, seguindo o ciclo
**Red → Green → Refactor**. O exercício consiste em implementar, com TDD, a
função `calcular_taxa_entrega(distancia_km, total_pedido)` em `src/pedido.py`.

## 1. Preparação do ambiente

Verifique a versão do Python (3.9 ou superior; o projeto foi executado com 3.14):

```powershell
python --version
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Confirme que o pytest está disponível:

```powershell
python -m pytest --version
```

Execute todos os testes a partir da raiz do projeto:

```powershell
python -m pytest -v
```

## 2. Exercício

Função implementada em `src/pedido.py`:

```python
calcular_taxa_entrega(distancia_km, total_pedido)
```

### Regras

- Até 3 km, a taxa de entrega é de R$ 5,00.
- Acima de 3 km, são acrescentados R$ 2,00 por quilômetro excedente.
- Pedidos a partir de R$ 100,00 possuem entrega gratuita.

### Cenários obrigatórios

| Distância | Pedido     | Taxa esperada | Teste                                              |
|-----------|------------|---------------|----------------------------------------------------|
| 2 km      | R$ 50,00   | R$ 5,00       | `test_cobra_taxa_inicial_ate_3_km`                 |
| 4 km      | R$ 50,00   | R$ 7,00       | `test_cobra_adicional_por_km_excedente`            |
| 5 km      | R$ 100,00  | R$ 0,00       | `test_entrega_gratis_para_pedido_a_partir_de_100`  |

### Desafio opcional

Distância negativa gera `ValueError`, coberto por
`test_rejeita_distancia_negativa`.

## 3. Processo TDD

Cada comportamento foi implementado isoladamente:

1. **Red:** escrever o teste e confirmar que ele falha.
2. **Green:** escrever apenas o código necessário para o teste passar e
   executar novamente toda a suíte.
3. **Refactor:** melhorar a estrutura do código sem alterar o comportamento,
   mantendo todos os testes passando.

As três regras não foram implementadas de uma só vez: o teste de cada cenário
foi escrito e visto falhando antes da implementação correspondente.

## 4. Registro

Os ciclos completos (Red, Green e Refactor de cada cenário, incluindo o desafio
opcional) estão em [`REGISTRO_TDD.md`](REGISTRO_TDD.md).

O resultado da execução dos testes está em
[`relatorio-testes.txt`](relatorio-testes.txt), gerado com:

```powershell
python -m pytest -v | Tee-Object -FilePath relatorio-testes.txt
```

## 5. Observação

Nesta aula as dependências foram instaladas diretamente no Python do sistema.
Na próxima aula será utilizado o `venv` para isolar os pacotes do projeto.
