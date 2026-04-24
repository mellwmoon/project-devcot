import flet as ft
from Utilities import lecture_util as lutil

class Lecture(ft.View):
  def __init__(self):

    cur_appbar = ft.AppBar(
      title=ft.Text(
        value="> DevCot",
        font_family="JetBrains Mono",
        theme_style=ft.TextThemeStyle.TITLE_MEDIUM
      ),
      leading_width=20,
      elevation=0,
      elevation_on_scroll=0,
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
                    spacing=20,
                    controls=[
                      ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                      ft.Text(
                        value="Account Settings",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_SMALL
                      )
                    ]
                  ),
                width=170
              )
            ),

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    spacing=20,
                    controls=[
                      ft.Icon(ft.Icons.SETTINGS),
                      ft.Text(
                        value="General Settings",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_SMALL
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
                    spacing=20,
                    controls=[
                      ft.Icon(ft.Icons.BOOK),
                      ft.Text(
                        value="References",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_SMALL
                      )
                    ]
                  ),
                width=200
              )
            ),

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    spacing=20,
                    controls=[
                      ft.Icon(ft.Icons.QUIZ),
                      ft.Text(
                        value="Excercises",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_SMALL
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
                    spacing=20,
                    controls=[
                      ft.Icon(ft.Icons.QUESTION_ANSWER),
                      ft.Text(
                        value="Help & Support",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_SMALL
                      )
                    ]
                  ),
                width=170
              )
            ),

            ft.PopupMenuItem(
              content=ft.Container(
                  content=ft.Row(
                    spacing=20,
                    controls=[
                      ft.Icon(ft.Icons.PERSON),
                      ft.Text(
                        value="About us",
                        font_family="JetBrains Mono",
                        theme_style=ft.TextThemeStyle.LABEL_SMALL
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

    # BODY =============================================

    container_list = ft.Container(
      width=450,
      padding=ft.Padding.only(left=10, right=10, top=5, bottom=5),
      # border=ft.Border.all(1, ft.Colors.WHITE),
      border_radius=10,
      content=ft.Column(
        height=600,
        scroll=ft.ScrollMode.AUTO,
        controls=[
          lutil.Item_Lecture("Heading"),
          lutil.Item_Lecture("Sub 1", is_heading=False),
          lutil.Item_Lecture("Sub 2", is_heading=False),
          lutil.Item_Lecture("Sub 3", is_heading=False),
          lutil.Item_Lecture("Heading 2"),
          lutil.Item_Lecture("Sub 1", is_heading=False),
          lutil.Item_Lecture("Heading 3", is_checked=True),
          lutil.Item_Lecture("Sub 1", is_heading=False, is_checked=True),
          lutil.Item_Lecture("Heading 4"),
          lutil.Item_Lecture("Sub 1", is_heading=False),
          lutil.Item_Lecture("Sub 2", is_heading=False),
          lutil.Item_Lecture("Sub 3", is_heading=False),
        ]
      )
    )

    container_desc = ft.Container(
      expand=True,
      padding=ft.Padding.only(left=10, right=10, top=5, bottom=5),
      border=ft.Border.all(1, ft.Colors.WHITE),
      content=ft.Column(
        controls=[

        ]
      )
    )

    body_content = ft.Row(
      spacing=20,
      controls=[
        container_list,
        container_desc
      ]
    )

    super().__init__(
      route="/lecture",
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.SafeArea(
          content=body_content,
          margin=30,
        )
      ],
      appbar=cur_appbar
    )