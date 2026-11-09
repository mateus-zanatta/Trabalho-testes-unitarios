"""Fixtures compartilhadas pelos testes funcionais."""

import re
import uuid

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


@pytest.fixture
def novo_usuario():
    """Dados de um usuario novo, com e-mail unico a cada execucao.

    O LocalEats nao permite dois cadastros com o mesmo e-mail, entao o e-mail
    recebe um sufixo aleatorio para que o teste possa ser repetido.
    """
    return {
        "nome": "Mateus Teste",
        "email": f"qa.{uuid.uuid4().hex[:10]}@teste.com",
        "senha": "senha123",
    }


@pytest.fixture
def pagina_logada(page, novo_usuario):
    """Cria uma conta pela interface e devolve a pagina ja autenticada.

    Todas as paginas do LocalEats exigem login, por isso esta etapa e uma
    pre-condicao dos testes que exploram a pagina inicial.
    """
    login = LoginPage(page)
    login.acessar()
    login.criar_conta(**novo_usuario)
    expect(page).to_have_url(re.compile(r"/index\.html$"))
    return page
