import flet as ft

class Home(ft.View):
    """
    A View subclass which shows the main home-page of the website.
    """
    
    DEFAULT_TITLE_SIZE = 100
    DEFAULT_TITLE_HEIGHT = 110
    DEFAULT_SUBTITLE_SIZE = 14

    def __init__(self):

        top_text = ft.Text(
            value="DEVCOT", 
            font_family="JetBrains Mono",
            size=self.DEFAULT_TITLE_SIZE,
            height=self.DEFAULT_TITLE_HEIGHT,
        )

        sub_text = ft.Text(
            value="Learn Development and Computer Technologies", 
            font_family="JetBrains Mono",
            size=self.DEFAULT_SUBTITLE_SIZE
        )

        top_button = ft.Button(content="Go to Second page", on_click=self.push_p2)

        header = ft.Column(
            margin=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                top_text,
                sub_text
            ]
        )

        super().__init__(
            route="/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                header
            ],
        )
    

    async def push_p2(self, e):
        await self.page.push_route("/page2")