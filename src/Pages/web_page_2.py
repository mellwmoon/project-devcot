import flet as ft
from Utilities import container_util as cutil

class Page2(ft.View):
    def __init__(self):
        self.page2_label_title = ft.Text("This is the second page")
        
        self.page2_button_back = ft.ElevatedButton(
            "Go back home", 
            on_click=self.push_home 
        )

        self.page2_header = ft.Column(
            controls=[
                self.page2_label_title,
                cutil.LayoutBox.create_bordered_container(),
                self.page2_button_back
            ]
        )

        self.page2_webui = ft.SafeArea(
            margin=10,
            content=self.page2_header
        )

        super().__init__(
            route="/page2",
            controls=[
                self.page2_webui
            ]
        )

    async def push_home(self, e):
        await self.page.push_route("/")