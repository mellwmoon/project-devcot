import flet as ft
from Pages import web_lecture as wel

# Note 1: markdown_area is where actual lesson's content are built in.

class Discuss(ft.View):

  def __init__(self):
    cur_appbar = wel.Lecture.load_appbar("test")

    content_area = ft.SafeArea(
      margin=10,
      content=ft.Container(
        margin=ft.Margin.only(left=150, right=150, top=40, bottom=0),
        padding=10,
        height=540,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        content=ft.Column(
          # expand=True,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[

            markdown_area:=ft.Column(
              spacing=0,
              expand=True,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              scroll=ft.ScrollMode.AUTO,
              width=700,
              # border=ft.Border.all(1, ft.Colors.WHITE),
            ),

            
            ft.Divider(),

            ft.FilledButton("Next", width=230),
            ft.Row(
              alignment=ft.MainAxisAlignment.CENTER,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              # expand=True,
              controls=[
                ft.Button("Back to list"),
                ft.Button("Previous"),
              ]
            )
          ]
        )
      )
    )

    lecture_markdown_style = ft.MarkdownStyleSheet(
        # --- Base Text (Paragraphs) ---
        p_text_style=ft.TextStyle(
            font_family="JetBrains Mono", 
            color=ft.Colors.WHITE70,
            size=14
        ),

        # --- Headers ---
        h1_text_style=ft.TextStyle(
            font_family="JetBrains Mono", 
            color=ft.Colors.GREEN_300,
            size=24, 
            weight=ft.FontWeight.BOLD
        ),
        h2_text_style=ft.TextStyle(
            font_family="JetBrains Mono", 
            color=ft.Colors.GREEN_100, 
            size=20,
            weight=ft.FontWeight.W_600
        ),

        # --- Headers ---
        code_text_style=ft.TextStyle(
            font_family="JetBrains Mono", 
            color=ft.Colors.GREEN_100, 
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_100) # Subtle green highlight
        ),
        
        # Multi-line code blocks
        # code_text_style=ft.TextStyle(
        #     font_family="JetBrains Mono", 
        #     color=ft.Colors.WHITE, 
        #     size=13
        # ),
    )

#     markdown_area.controls.append(ft.Markdown("""
# # Computer Engineering
# ## What is it?
# It is a field of study that does engineering on computers :)
# ![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgVfHORQFLyUf_rNove-xUmxIskDeMJ63REz_YIMQ6S0vCyQdkBvJos4igKspvCgpqnpy8h0xM--1uckzZIxDgyoHy37-MowkF-YzvVx8&s=10)



# """, md_style_sheet=lecture_markdown_style,
#     ))
    

    super().__init__(
      appbar=cur_appbar,
      controls=content_area
    )