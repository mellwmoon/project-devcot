import flet as ft
from Pages import web_lecture as wel

class Discuss(ft.View):

  def __init__(self):
    cur_appbar = wel.Lecture.load_appbar("test")

    content_area = ft.SafeArea(
      margin=10,
      content=ft.Container(
        padding=10,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        content=ft.Column(
          controls=[
            ft.FilledButton("<"),

            ft.Container(
              expand=True,
              border=ft.Border.all(1, ft.Colors.WHITE),
              content=(con_area:=ft.Column(
                expand=True,

              ))
            ),

            ft.Row(
              alignment=ft.MainAxisAlignment.CENTER,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              expand=True,
              controls=[
                ft.Button("Previous"),
                ft.FilledButton("Next")
              ]
            )
          ]
        )
      )
    )

    super().__init__(
      appbar=cur_appbar,
      controls=content_area
    )