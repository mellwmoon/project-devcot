import flet as ft
from Utilities import container_util as cutil

class Home(ft.View):
    """
    A View subclass which shows the main home-page of the website.
    """
    
    TITLE_SIZE = 100
    TITLE_HEIGHT = 110
    SUBTITLE_SIZE = 14
    
    BUTTON_SIZE = 20
    BUTTON_RADIUS = 20
    BUTTON_TEXT_SIZE = 20

    COL_TITLE = '#a4ff4a'
    COL_SUBTITLE = "#8eac48"
    COL_BUTTON = "#bbff7b"
    COL_BG = "#041015"

    def __init__(self):
        top_text = ft.Text(
            value="DEVCOT", 
            font_family="JetBrains Mono",
            size=self.TITLE_SIZE,
            height=self.TITLE_HEIGHT,
            color=self.COL_TITLE
        )

        sub_text = ft.Text(
            value="Learn Development and Computer Technologies", 
            font_family="JetBrains Mono",
            size=self.SUBTITLE_SIZE,
            color=self.COL_SUBTITLE
        )

        button_nextmain = ft.ElevatedButton(
            content=ft.Text(
                value="Learn",
                color=self.COL_BUTTON,
                font_family="JetBrains Mono",
                size=self.BUTTON_TEXT_SIZE
            ), 
            on_click=self.push_p2,
            margin=30,
            width=300,
            height=70,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=self.BUTTON_RADIUS),
                side=ft.BorderSide(2, self.COL_BUTTON),
                bgcolor=ft.Colors.TRANSPARENT
            )
        )

        content = ft.Column(
            margin=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                top_text,
                sub_text,
                button_nextmain,
            ]
        )

        super().__init__(
            route="/",
            bgcolor=self.COL_BG,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                content
            ],
        )
    

    async def push_p2(self, e):
        await self.page.push_route("/page2")