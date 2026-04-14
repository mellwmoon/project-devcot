import flet as ft
from Utilities import container_util as cutil
from Utilities import effect_util as efutil

class Home(ft.View):
    """
    A View subclass which shows the main home-page of the website.
    """
    
    TITLE_SIZE = 150
    TITLE_HEIGHT = 160
    SUBTITLE_SIZE = 30
    
    BUTTON_SIZE = 20
    BUTTON_RADIUS = 20
    BUTTON_TEXT_SIZE = 25
    BUTTON_SPACE = 90

    COL_TITLE = '#a4ff4a'
    COL_SUBTITLE = "#8eac48"

    COL_BUTTON = "#bbff7b"
    COL_BUTTON_BG = "#041015"

    def __init__(self):
        top_text = ft.Text(
            value="> DEVCOT", 
            font_family="JetBrains Mono",
            style=ft.TextThemeStyle.DISPLAY_LARGE,
            height=self.TITLE_HEIGHT,
        )

        anim_top_text = efutil.Fun(
            text_value="> DEVCOT", 
            text_size=self.TITLE_SIZE,
            caret_type="_",
            is_caret_colored=True
        )

        sub_text = ft.Text(
            value="Learn Development and Computer Technologies", 
            font_family="JetBrains Mono",
            theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
            size=self.SUBTITLE_SIZE,
        )

        button_nextmain = ft.FilledButton(
            content=ft.Text(
                value="Learn -->",
                font_family="JetBrains Mono",
                size=self.BUTTON_TEXT_SIZE,
            ), 
            on_click=self.push_p2,
            margin=self.BUTTON_SPACE,
            width=300,
            height=70,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=self.BUTTON_RADIUS),
            )
        )

        content = ft.Column(
            margin=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                anim_top_text,
                sub_text,
                button_nextmain,
            ]
        )

        super().__init__(
            route="/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                content
            ],
        )
    

    async def push_p2(self, e):
        await self.page.push_route("/login")