import flet as ft
from Utilities import effect_util as efutil


class Signup(ft.View):



  def __init__(self):

    m_anim_title = efutil.Fun("> Sign_up", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)
    
    input_container = ft.Row(
      margin=10,
      controls=[
        ft.Column(
          
        ),
        ft.Column(
          
        )
      ]
    )

    main_layout = ft.Column(
      margin=10,
      controls=[
        
      ],
    )
  
    super().__init__(
      route="/signup",
      controls=[
        
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
