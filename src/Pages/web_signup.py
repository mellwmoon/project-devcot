import flet as ft
from Utilities import effect_util as efutil


class Signup(ft.View):

  INPUT_CONTAINER_WIDTH = 500
  INPUT_ROUNDED_BORDER_RAD = 5

  def __init__(self):

    m_anim_title = efutil.Fun("> Sign_up", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)
    
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
                        ft.Text("Display Name", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                        self.create_field("Username"),                        
                        ft.Text("Email", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                        self.create_field("Email"),
                        ft.Text("Password ", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                        self.create_field("Password", True),
                        ft.Text("Age ", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                        self.create_field("Age"),
                        ft.Text("Birthday", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                        self.create_field("01/03/12"),
                        ft.Text("University Email (Optional)", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
                        self.create_field("reichard@univeristy.org"),
                    ]
                )
            ]
        )
    )

    main_layout = ft.Column(
      margin=10,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        m_anim_title,
        input_fields_container
      ],
    )
  
    super().__init__(
      route="/signup",
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        main_layout
      ]
    )


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
