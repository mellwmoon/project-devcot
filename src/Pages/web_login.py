import asyncio
import flet as ft
from Utilities import container_util as cutil
from Utilities import effect_util as efutil
from Utilities import database_util as dabil

class Login(ft.View):

    TITLE_SIZE = 40
    TITLE_HEIGHT = 110
    SUBTITLE_SIZE = 14

    INPUT_CONTAINER_WIDTH = 400
    INPUT_ROUNDED_BORDER_RAD = 20

    COL_BG = "#041015"

    def __init__(self, db:dabil.DatabaseManager):
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
                            field_user:=self.create_field("Email or User"),
                            ft.Text("Password ", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                            field_password:=self.create_field("Password", True),
                        ]
                    )
                ]
            )
        )

        async def _on_submit(e):
            r=None

            await _process_idle_wait()

            if field_password.value is "" and field_user.value is "":
                # print("ERROR: NO INPUT FIELDS - DENYING.")
                self.page.show_dialog(ft.SnackBar(ft.Text("Input fields are Empty!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
                return
            elif field_password.value is "":
                # print("ERROR: NO PASSWORD - DENYING.")
                self.page.show_dialog(ft.SnackBar(ft.Text("Password field is Empty!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
                return
            elif field_user.value is "":
                # print("ERROR: NO USER - DENYING.")
                self.page.show_dialog(ft.SnackBar(ft.Text("User field is Empty!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
                return
            else:
                r=db.verify_user_logon(field_user.value, field_password.value)


            await _process_idle_wait(1)

# ======================= IMPORTANT ===========================
            if not r: # Fail part
                self.page.show_dialog(ft.SnackBar(ft.Text("Username/Email or Password is Incorrect", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))

            else: # Success part
                self.page.show_dialog(ft.SnackBar(ft.Text("Welcome!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
                await self.page.shared_preferences.set("current_user", field_user.value)
                await self.page.shared_preferences.set("")
                await self.push_library(e)
# =======================     o     ===========================
        
        async def _process_idle_wait(dur_sec=0.6):
            
            main_content.opacity -= 0.4
            button_submit.disabled = True
            button_signup.disabled = True
            self.page.update()

            await asyncio.sleep(dur_sec)

            main_content.opacity = 1
            button_submit.disabled = False
            button_signup.disabled = False
            self.page.update()
                
                

        button_submit = ft.FilledButton(
            content=ft.Text(
                value="Login",
                font_family="JetBrains Mono"
            ),
            on_click=_on_submit
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
                        button_signup:=ft.Button(
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
    async def push_library(self, e):
        await self.page.push_route("/library")

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
