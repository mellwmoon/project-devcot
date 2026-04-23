import flet as ft

class Lecture(ft.View):
  def __init__(self):

    cur_appbar = ft.AppBar(
      title=ft.Text(
        value="> DevCot",
        font_family="JetBrains Mono",
        theme_style=ft.TextThemeStyle.TITLE_MEDIUM
      ),
      leading_width=20,
      bgcolor=ft.Colors.BLACK_45,
      color=ft.Colors.GREEN_300,
      actions=[
        ft.PopupMenuButton(
          margin=ft.Margin.only(right=20),
          menu_padding=8,
          menu_position=ft.PopupMenuPosition.UNDER,
          items=[
            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    controls=[
                      ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                      ft.Text(
                        value="Account Settings",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                      )
                    ]
                  ),
                width=170
              )
            ),

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    controls=[
                      ft.Icon(ft.Icons.SETTINGS),
                      ft.Text(
                        value="General Settings",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                      )
                    ]
                  ),
                width=200
              )
            ),

# DIVIDER =========================      
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),
# DIVIDER =========================

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    controls=[
                      ft.Icon(ft.Icons.BOOK),
                      ft.Text(
                        value="References",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                      )
                    ]
                  ),
                width=200
              )
            ),

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    controls=[
                      ft.Icon(ft.Icons.QUIZ),
                      ft.Text(
                        value="Excercises",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                      )
                    ]
                  ),
                width=200
              )
            ),

# DIVIDER =========================      
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),
# DIVIDER =========================

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    controls=[
                      ft.Icon(ft.Icons.QUESTION_ANSWER),
                      ft.Text(
                        value="Help & Support",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                      )
                    ]
                  ),
                width=170
              )
            ),

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    controls=[
                      ft.Icon(ft.Icons.PERSON),
                      ft.Text(
                        value="About us",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_MEDIUM
                      )
                    ]
                  ),
                width=170
              )
            ),
          ],
        )
      ],

    )




    super().__init__(
      route="/lecture",
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[

      ],
      appbar=cur_appbar
    )