# Atividade 4: Testes Automatizados do LocalEats

## 1. Identificação

| Campo | Valor |
|---|---|
| Unidade Curricular | Qualidade de Software |
| Projeto | LocalEats |
| Modalidade | Individual |
| Integrante | Mateus Zanatta Mariani |
| Sistema testado | <https://local-eats-unisenac.vercel.app/> |

## 2. Estrutura do diretório

```text
atividade-04/
├── atividade-04-testes-automatizados.md   # este documento
├── relatorio-pytest.txt                   # saída do pytest -v
├── requirements.txt                       # dependências
├── pytest.ini                             # configuração do pytest
├── src/
│   ├── __init__.py
│   └── regras_localeats.py                # Regra 1 (valor mínimo do pedido)
├── pages/                                 # Page Object Model (diferencial)
│   ├── __init__.py
│   ├── login_page.py
│   └── home_page.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                        # fixtures dos testes funcionais
│   ├── test_regras_localeats.py           # testes unitários
│   └── test_localeats.py                  # testes funcionais (Playwright)
└── evidencias/                            # screenshots gerados pelos testes
```

## 3. Como executar

No PowerShell, a partir da raiz do repositório:

```powershell
cd atividades\atividade-04
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

- `python -m playwright install chromium` baixa o navegador usado pelo
  Playwright. Só é necessário na primeira vez.
- Por padrão os testes funcionais rodam com o navegador invisível (*headless*).
  Para assistir à execução, use `python -m pytest -v --headed --slowmo 500`.
- O `pytest.ini` define `testpaths = tests` e `pythonpath = .`, por isso o
  comando deve ser executado dentro de `atividades\atividade-04`.

## 4. Identificação das responsabilidades

| ID | Integrante | Tipo | Comportamento verificado | Arquivo e função |
|---|---|---|---|---|
| TU01 | Mateus Zanatta Mariani | Unitário | Pedido acima do mínimo (R$ 50,00) atinge o valor mínimo | `tests/test_regras_localeats.py::test_pedido_acima_do_minimo_atinge_valor_minimo` |
| TU02 | Mateus Zanatta Mariani | Unitário | Pedido abaixo do mínimo (R$ 20,00) não atinge o valor mínimo | `tests/test_regras_localeats.py::test_pedido_abaixo_do_minimo_nao_atinge_valor_minimo` |
| TU03 | Mateus Zanatta Mariani | Unitário | Limite de R$ 30,00: R$ 29,99 retorna `False` e R$ 30,00 retorna `True` (parametrizado) | `tests/test_regras_localeats.py::test_limite_do_valor_minimo_de_30_reais` |
| TU04 | Mateus Zanatta Mariani | Unitário | Valor negativo gera `ValueError` | `tests/test_regras_localeats.py::test_valor_negativo_gera_value_error` |
| TF01 | Mateus Zanatta Mariani | Funcional | Criar conta, entrar no sistema e ver a página inicial | `tests/test_localeats.py::test_criar_conta_entra_no_sistema_e_exibe_pagina_inicial` |
| TF02 | Mateus Zanatta Mariani | Funcional | Filtrar pela categoria Japonesa e exibir só restaurantes japoneses | `tests/test_localeats.py::test_filtro_japonesa_exibe_somente_restaurantes_japoneses` |

Observações sobre o relatório:

- O TU03 é parametrizado, então aparece duas vezes no `relatorio-pytest.txt`:
  `[29.99-False]` e `[30-True]`.
- Os testes funcionais aparecem com o sufixo `[chromium]`, que indica o
  navegador usado pelo plugin `pytest-playwright`.

## 5. Parte 1: Testes unitários e TDD

### Regra escolhida

**Regra 1: verificar valor mínimo do pedido**, com a função
`pedido_atingiu_valor_minimo(valor_pedido)`:

- pedidos de R$ 30,00 ou mais retornam `True`;
- pedidos abaixo de R$ 30,00 retornam `False`;
- valores negativos geram `ValueError`.

Implementação final (`src/regras_localeats.py`):

```python
VALOR_MINIMO_PEDIDO = 30


def pedido_atingiu_valor_minimo(valor_pedido):
    if valor_pedido < 0:
        raise ValueError("O valor do pedido nao pode ser negativo.")

    return valor_pedido >= VALOR_MINIMO_PEDIDO
```

### TDD de Mateus Zanatta Mariani

**Regra escolhida:** Regra 1, verificar valor mínimo do pedido
(`pedido_atingiu_valor_minimo`).

**Primeiro teste escrito:** `test_pedido_acima_do_minimo_atinge_valor_minimo`
(TU01). Chama a função com `50` e espera `True`.

**Por que o teste falhou inicialmente:** a função ainda não existia. O arquivo
`src/regras_localeats.py` tinha apenas a docstring, então o pytest não
conseguiu nem coletar o teste:

```text
E   ImportError: cannot import name 'pedido_atingiu_valor_minimo' from 'src.regras_localeats'
```

**Implementação mínima realizada:** foi criada a função retornando sempre
`True`. É o mínimo para o TU01 passar, mesmo sem cumprir a regra ainda.

```python
def pedido_atingiu_valor_minimo(valor_pedido):
    return True
```

**Segundo teste escrito:** `test_pedido_abaixo_do_minimo_nao_atinge_valor_minimo`
(TU02). Chama a função com `20` e espera `False`. Ele falhou com
`assert True is False`, porque a implementação mínima ignorava o valor. A
implementação foi ajustada para `return valor_pedido >= 30`, e os dois testes
passaram.

**Testes adicionais (diferenciais):**

- **TU03, caso de borda:** testa `29.99 → False` e `30 → True` com
  `@pytest.mark.parametrize`. Ele passou na primeira execução porque a
  comparação já era `>=`. Mesmo assim, ele protege o limite: se alguém trocar
  `>=` por `>`, o caso `30 → True` falha.
- **TU04, exceção:** usa `pytest.raises(ValueError, match="negativo")` com
  `-10`. Falhou com `Failed: DID NOT RAISE ValueError`, porque ainda não havia
  validação. Foi adicionado o `if valor_pedido < 0: raise ValueError(...)` no
  início da função, e o teste passou.

**Melhoria ou refatoração realizada:** o número `30`, que estava fixo no
código, virou a constante `VALOR_MINIMO_PEDIDO`, e a função ganhou uma
docstring explicando a regra. O comportamento não mudou: os 5 casos
continuaram passando.

Cada etapa foi registrada em um commit separado no histórico do repositório.
As mensagens começam com `TDD (red)`, `TDD (green)` e `TDD (refactor)`.

## 6. Parte 2: Testes funcionais com Playwright

### O que foi observado na exploração do LocalEats

- O endereço principal redireciona para `/static/index.html`.
- **Todas as páginas exigem login.** O script `js/auth.js` manda para
  `login.html` quem não tem `userId` no `localStorage`. Por isso, os testes
  funcionais precisam criar uma conta antes de usar a página inicial.
- A tela `login.html` tem as abas **Entrar** e **Criar Conta**. Os `<label>`
  dos campos não estão ligados aos `<input>` (falta o atributo `for`), então
  `get_by_label` não funciona. Os campos foram localizados pelo *placeholder*:
  "Seu nome", "novo@teste.com" e "Min. 3 caracteres".
- Depois do cadastro, o sistema vai para `index.html` e o cabeçalho mostra
  "Olá, <primeiro nome>".
- A página inicial tem os botões de categoria **Todos, Italiana, Japonesa,
  Brasileira e Mexicana**. Cada restaurante aparece como um card (`.rest-card`)
  com nome, culinária e localização.

### TF01: criar conta e entrar no sistema

Fluxo:

1. acessar `login.html`;
2. clicar na aba **Criar Conta**;
3. preencher nome, um e-mail único e a senha;
4. clicar em **Registrar**.

Assertions:

| Assertion | O que garante |
|---|---|
| `expect(page).to_have_url(re.compile(r"/index\.html$"))` | o cadastro funcionou e o sistema levou o usuário para a página inicial |
| `expect(home.saudacao_usuario).to_contain_text("Olá, Mateus")` | o usuário está logado com o nome cadastrado |
| `expect(home.titulo).to_be_visible()` | a página inicial foi exibida ("Descubra sabores incríveis na sua cidade") |

O e-mail é gerado com `uuid` (ex.: `qa.3f9a1c0b2e@teste.com`) porque o
LocalEats não aceita dois cadastros com o mesmo e-mail. Assim, o teste pode ser
executado várias vezes.

### TF02: filtrar restaurantes pela categoria Japonesa

Fluxo:

1. criar conta e entrar (fixture `pagina_logada`);
2. esperar a lista inicial de restaurantes carregar;
3. clicar no botão **Japonesa**.

Assertions:

| Assertion | O que garante |
|---|---|
| `expect(botao Japonesa).to_have_class(re.compile(r"\bactive\b"))` | o filtro selecionado fica destacado |
| `expect(cards.first).to_contain_text("Japonesa")` | a lista foi recarregada com o resultado do filtro |
| `expect(cards.filter(has_not_text="Japonesa")).to_have_count(0)` | nenhum restaurante de outra culinária aparece |

### Page Object Model (diferencial)

Os locators ficam nas classes de `pages/`, e os testes só chamam ações com
nomes legíveis:

- `LoginPage`: `acessar()` e `criar_conta(nome, email, senha)`;
- `HomePage`: `saudacao_usuario`, `titulo`, `cards_restaurantes`,
  `botao_categoria(nome)` e `filtrar_por_categoria(nome)`.

Se a tela mudar (por exemplo, o placeholder de um campo), a correção é feita em
um único lugar. As **assertions continuam dentro dos testes**, não nos Page
Objects, para que cada teste mostre claramente o que verifica.

### Sem `time.sleep`

Nenhum teste usa `time.sleep`. O Playwright espera sozinho pelos elementos
antes de clicar ou preencher (*auto-wait*). O `expect(...)` tenta a verificação
de novo, por até 5 segundos, até ela passar. Assim o teste espera apenas o
tempo necessário, e não um tempo fixo.

### Evidências

Os testes salvam screenshots em `evidencias/`:

- `TF01-conta-criada.png`: página inicial depois do cadastro;
- `TF02-filtro-japonesa.png`: página inteira com o filtro Japonesa aplicado.

## 7. Explicação individual: TF02

**Teste:** `test_filtro_japonesa_exibe_somente_restaurantes_japoneses`

O teste segue o padrão **Arrange, Act, Assert**:

- **Arrange (preparação):** a fixture `pagina_logada`, do `conftest.py`, cria
  uma conta nova pela interface e devolve a página já logada. Em seguida, o
  teste espera o primeiro card de restaurante aparecer. Essa espera evita um
  problema de concorrência: ao abrir, a página faz uma busca **sem filtro**. Se
  o clique em "Japonesa" acontecesse antes dessa busca terminar, a resposta sem
  filtro poderia chegar por último e sobrescrever a lista filtrada.
- **Act (ação):** clica no botão "Japonesa", localizado com
  `get_by_role("button", name="Japonesa", exact=True)`. O `exact=True` evita
  pegar outro botão que só contenha a palavra.
- **Assert (verificação):**
  1. o botão "Japonesa" recebe a classe `active`, ou seja, fica destacado;
  2. o primeiro card passa a conter "Japonesa". Antes do filtro, o primeiro
     card é um restaurante italiano, então essa verificação também serve para
     esperar a lista nova ser desenhada;
  3. a quantidade de cards **sem** o texto "Japonesa" é zero. Essa verificação
     só é feita depois da anterior. Se fosse feita durante o carregamento, com
     a lista vazia, ela passaria sem ter testado nada.

**Como foi confirmado que o teste realmente testa o filtro:** o clique em
"Japonesa" foi removido de propósito em uma cópia temporária do teste. O teste
falhou (`Locator expected to have class ... Actual value: filter-btn`). Isso
mostra que ele não passa "por acaso".

## 8. Diferenciais implementados

- [x] terceiro teste unitário para um caso de borda (TU03: R$ 29,99 e R$ 30,00);
- [x] uso de `pytest.raises` para verificar uma exceção (TU04);
- [x] parametrização com `pytest.mark.parametrize` (TU03);
- [x] organização com Page Object Model (`pages/`);
- [x] segundo teste funcional pelo mesmo integrante (TF02);
- [x] screenshot da execução (`evidencias/`);
- [x] registro de falhas encontradas (seção 9).

## 9. Falhas encontradas

### Defeito encontrado no LocalEats: a busca não encontra culinárias

O campo de busca da página inicial diz **"Buscar por culinária ou
localização..."**, mas só funciona com localização:

| Termo buscado | Resultado na tela |
|---|---|
| `Centro` | 4 restaurantes |
| `Japonesa` | "Nenhum restaurante encontrado." (existem 5 restaurantes japoneses) |

**Causa (em `js/app.js`):** o texto digitado é sempre enviado como
`currentFilters.location`. A API recebe `?location=Japonesa` e não acha nenhuma
localização com esse nome. O defeito pertence ao sistema testado e não pode ser
corrigido neste repositório. Por isso ele não foi transformado em teste
automatizado, para não deixar a suíte vermelha por um problema conhecido.

### Falha corrigida nos testes

A primeira versão do TF02 salvava o screenshot só da parte visível da tela. A
imagem mostrava o botão "Japonesa" ativo, mas não os cards filtrados, então não
servia como evidência do resultado. A correção foi usar
`page.screenshot(..., full_page=True)`.

## 10. Uso de inteligência artificial

**Ferramenta utilizada:** Claude Code (Anthropic).

**Como a ferramenta foi utilizada:**

- leitura do enunciado da atividade e montagem da estrutura de pastas;
- exploração do HTML e do JavaScript do LocalEats para entender o fluxo de
  login e escolher os locators;
- escrita dos testes e da função seguindo o ciclo TDD, executando o pytest a
  cada etapa e salvando cada etapa em um commit;
- redação deste documento.

**Uma sugestão que precisou ser alterada ou rejeitada:**

- Localizar os campos do cadastro com `get_by_label("E-mail")` foi descartado.
  Os `<label>` do LocalEats não estão associados aos `<input>`, então o locator
  não encontraria os campos. Foi usado `get_by_placeholder`.
- O screenshot do TF02 foi alterado para página inteira (`full_page=True`),
  porque a primeira versão não mostrava os cards filtrados.
- Arquivos de cache do Python (`__pycache__`) chegaram a entrar nos commits. Eles
  foram removidos do histórico e foi criado um `.gitignore`.

**Como o código sugerido foi verificado:**

- execução de `python -m pytest -v` após cada mudança;
- confirmação de que cada teste novo **falhava antes** da implementação (etapa
  *red* do TDD);
- teste de mutação manual no TF02: sem o clique no filtro, o teste falha;
- conferência visual dos screenshots em `evidencias/`;
- conferência, direto na API do LocalEats, dos restaurantes japoneses e do
  resultado da busca.

## 11. Relatório da execução

O arquivo [`relatorio-pytest.txt`](relatorio-pytest.txt) foi gerado com:

```powershell
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

Resultado: **7 testes coletados e 7 aprovados**. São 5 execuções unitárias
(TU01, TU02, TU03 com 2 casos e TU04) e 2 funcionais (TF01 e TF02).
