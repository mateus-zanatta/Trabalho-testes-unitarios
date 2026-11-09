"""Page Object da tela de login/cadastro do LocalEats."""

from playwright.sync_api import Page

URL_LOGIN = "https://local-eats-unisenac.vercel.app/static/login.html"


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.aba_criar_conta = page.get_by_role("button", name="Criar Conta")
        # Os <label> da tela nao estao ligados aos campos (sem atributo "for"),
        # por isso os campos sao localizados pelo placeholder.
        self.campo_nome = page.get_by_placeholder("Seu nome")
        self.campo_email = page.get_by_placeholder("novo@teste.com")
        self.campo_senha = page.get_by_placeholder("Min. 3 caracteres")
        self.botao_registrar = page.get_by_role("button", name="Registrar")

    def acessar(self):
        self.page.goto(URL_LOGIN)

    def criar_conta(self, nome, email, senha):
        self.aba_criar_conta.click()
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_senha.fill(senha)
        self.botao_registrar.click()
