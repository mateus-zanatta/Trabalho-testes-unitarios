"""Page Object da pagina inicial (Explorar) do LocalEats."""

from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.saudacao_usuario = page.locator("#userBadge")
        self.titulo = page.get_by_role(
            "heading", name="Descubra sabores incríveis na sua cidade"
        )
        self.cards_restaurantes = page.locator(".rest-card")

    def botao_categoria(self, categoria):
        return self.page.get_by_role("button", name=categoria, exact=True)

    def filtrar_por_categoria(self, categoria):
        self.botao_categoria(categoria).click()
