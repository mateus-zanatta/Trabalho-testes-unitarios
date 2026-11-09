# Responsável: Mateus Zanatta Mariani
# Testes funcionais do LocalEats com Playwright (Page Object Model).

import re
from pathlib import Path

from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.login_page import LoginPage

PASTA_EVIDENCIAS = Path(__file__).resolve().parent.parent / "evidencias"


# TF01
def test_criar_conta_entra_no_sistema_e_exibe_pagina_inicial(
    page: Page, novo_usuario
):
    # Arrange
    login = LoginPage(page)
    home = HomePage(page)
    login.acessar()

    # Act
    login.criar_conta(
        novo_usuario["nome"], novo_usuario["email"], novo_usuario["senha"]
    )

    # Assert
    expect(page).to_have_url(re.compile(r"/index\.html$"))
    expect(home.saudacao_usuario).to_contain_text("Olá, Mateus")
    expect(home.titulo).to_be_visible()
    page.screenshot(path=PASTA_EVIDENCIAS / "TF01-conta-criada.png")


# TF02 (diferencial: segundo teste funcional do mesmo integrante)
def test_filtro_japonesa_exibe_somente_restaurantes_japoneses(pagina_logada: Page):
    # Arrange
    home = HomePage(pagina_logada)
    # Espera a lista inicial carregar antes de filtrar, para que a resposta
    # da busca inicial nao sobrescreva o resultado do filtro.
    expect(home.cards_restaurantes.first).to_be_visible()

    # Act
    home.filtrar_por_categoria("Japonesa")

    # Assert
    expect(home.botao_categoria("Japonesa")).to_have_class(re.compile(r"\bactive\b"))
    expect(home.cards_restaurantes.first).to_contain_text("Japonesa")
    expect(
        home.cards_restaurantes.filter(has_not_text="Japonesa")
    ).to_have_count(0)
    pagina_logada.screenshot(
        path=PASTA_EVIDENCIAS / "TF02-filtro-japonesa.png", full_page=True
    )
