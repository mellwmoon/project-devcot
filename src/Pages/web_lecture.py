import flet as ft
from Utilities import lecture_util as lutil


# Note 1: content_lecture_list -> Main list container
# Note 2: container_desc -> Main Description container,
#         use lutil.ContentLecture to create details about lecture.

class Lecture(ft.View):

  TOPIC_SELECTED = "TOPIC PLACEHOLDER"

  def __init__(self):
    
    cur_appbar = self.load_appbar(self.TOPIC_SELECTED)

    # BODY =============================================

    container_list = ft.Container(
      width=450,
      padding=ft.Padding.only(left=10, right=10, top=5, bottom=5),
      # margin=ft.Margin.only(right=90),
      # border=ft.Border.all(1, ft.Colors.WHITE),
      border_radius=10,
      content=ft.Column(
        height=600,
        
        scroll=ft.ScrollMode.ADAPTIVE,
        controls=ft.Container(
          border_radius=10,
          padding=ft.Padding.only(right=16),
          content=(content_lecture_list:=ft.Column(
            controls=[]
          ))
        )
      )
    )

    container_desc = ft.Container(
      expand=True,
      padding=ft.Padding.only(left=20, right=20, top=15, bottom=15),
      border_radius=10,
      border=ft.Border.all(1.5, ft.Colors.GREEN_300),
      content=lutil.ContentLecture(
        title="No Content",
        description="No Content",
        topics_amount=0,
        excercises_amount=0,
        topics_taken=0,
        excercises_taken=0,
      )
    )

    body_content = ft.Row(
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=20,
      controls=[
        container_list,
        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          expand=True, 
          controls=[
            container_desc,
            ft.FilledButton(
              margin=ft.Margin.only(top=15),
              height=50,
              width=230,
              content=ft.Text("Study ->", font_family="JetBrains Mono", weight=ft.FontWeight.W_700, size=18)
            ),
            ft.OutlinedButton(
              margin=ft.Margin.only(top=6),
              height=50,
              width=150,
              content=ft.Text("Go Back", font_family="JetBrains Mono", weight=ft.FontWeight.W_700, size=18)
            ),
          ]
        ),
      ]
    )

    super().__init__(
      route="/lecture",
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.SafeArea(
          content=body_content,
          margin=5,
        )
      ],
      appbar=cur_appbar
    )


  def load_lecture(topics:dict, ) -> None:
    """
    Parameters:
      topics : Dictionary
        In a format of [Lesson : Sub-topic].
        Sub-topics are lists.
    """
    pass

  @classmethod
  def load_appbar(self, topic_selected:str="", is_appbar_only=False) -> load_appbar:
    return ft.AppBar(
      title=ft.Text(
        value=f"> DevCot: {topic_selected}" if not is_appbar_only else "> DevCot",
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