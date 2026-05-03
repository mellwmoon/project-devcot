import flet as ft
from Utilities import container_util as cutil
from Utilities import effect_util as efutil

class Login(ft.View):

    TITLE_SIZE = 40
    TITLE_HEIGHT = 110
    SUBTITLE_SIZE = 14

    INPUT_CONTAINER_WIDTH = 400
    INPUT_ROUNDED_BORDER_RAD = 20

    COL_BG = "#041015"

    def __init__(self, dbMan):
        m_anim_title = efutil.Fun("> Sign_in", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)

        input_fields_container = ft.Container(
            width=self.INPUT_CONTAINER_WIDTH,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        margin=10,
                        controls=[
                            ft.Text("Email or Username", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                            self.create_field("Email or User"),
                            ft.Text("Password ", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                            self.create_field("Password", True),
                        ]
                    )
                ]
            )
        )

        button_submit = ft.FilledButton(
            content=ft.Text(
                value="Login",
                font_family="JetBrains Mono"
            )
        )


        main_content    = ft.Column(
            margin=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                m_anim_title,
                input_fields_container,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        button_submit
                    ]
                ),
                ft.Column(
                    margin=50,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="Don't have an account yet?", 
                            font_family="JetBrains Mono",
                            size=12,
                            margin=0,
                            theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                        ),
                        ft.Button(
                            content=ft.Text(
                                value="Sign up!",
                                font_family="JetBrains Mono",
                                size=12,
                            ), 
                            style=ft.ButtonStyle(
                                side=ft.RoundedRectangleBorder(radius=1),
                                
                            ),
                            margin=0,
                            width=120,
                            height=30,
                            on_click=self.push_signup
                        )
                    ]
                )
            ]
        )

        super().__init__(
            route="/login",
            bgcolor=self.COL_BG,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=main_content
        )

    async def push_home(self, e):
        await self.page.push_route("/")
    
    async def push_signup(self, e):
        await self.page.push_route("/signup")

    def create_field(self, hint_text, is_password=False) -> ft.TextField:
        return ft.TextField(
            password=is_password,
            autofill_hints=True,
            can_reveal_password=True,
            multiline=False,
            expand=True,
            hint_text=hint_text,
            border=ft.RoundedRectangleBorder(radius=self.INPUT_ROUNDED_BORDER_RAD),
            content_padding=0,
            border_color=ft.Colors.WHITE,
            height=50,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            hint_style=ft.TextStyle(
                    color="#363636",
                    font_family="JetBrains Mono",
                    size=14,
            ),
            text_style=ft.TextStyle(
                    color="#FFFFFF",
                    font_family="JetBrains Mono",
                    size=14,
            ),
        )
