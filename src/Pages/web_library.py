import flet as ft
from Pages import web_lecture as wel
from Utilities import data_util

# Note 1: content_inner is where you place Libraries (Lectures)

class Library(ft.View):

  def __init__(self):
    cur_appbar = wel.Lecture.load_appbar(is_appbar_only=True)

    main_body = ft.Column(
      expand=True,
      scroll=ft.ScrollMode.ADAPTIVE,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        
        content_inner:=ft.Row(
          expand=True,
          wrap=True,
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[]
        )

      ]
    )

    content_area = ft.SafeArea(
      margin=10,
      content=ft.Container(
        expand=True,
        # border=ft.Border.all(1, ft.Colors.WHITE),
        content=main_body,
        alignment=ft.Alignment.CENTER,
        padding=10,
        height=540,
      )
    )

    header_area = ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.START,
      margin=ft.Margin.only(top=10),
      controls=[
        ft.Text("Current Library", theme_style=ft.TextThemeStyle.TITLE_LARGE, font_family="JetBrains Mono"),
        ]
    )
    
    # DYNAMIC PAYLOAD LOADING
    saved_lectures = data_util.load_all_lectures()

    for lec in saved_lectures:
        
        # Must be async to use await push_route!
        async def block_clicked(e, payload=lec):
            # 1. Stash the entire dictionary payload into the user's session backpack
            e.page.session.store.set("current_lecture_payload", payload)
            
            # 2. Async routing to the lecture page
            await e.page.push_route("/lecture")

        # Safely convert the string icon name from JSON back into an ft.Icons enum
        icon_name = lec.get("icon", "BOOK").upper()
        icon_enum = getattr(ft.Icons, icon_name, ft.Icons.BOOK)

        content_inner.controls.append(
            self.create_lecture(
                lecture_icon=ft.Icon(icon_enum, size=30),
                lecture_text=lec.get("title", "Untitled Lecture"),
                description=lec.get("description", "No description provided."),
                amount_topics=lec.get("topics_amount", 0),
                amount_excercise=lec.get("exercises_amount", 0),
                amount_videos=lec.get("videos_amount", 0),
                on_block_click=block_clicked
            )
        )

    super().__init__(
      appbar=cur_appbar,
      vertical_alignment=ft.MainAxisAlignment.START,
      spacing=10,
      controls=[
        header_area,
        content_area
      ],
    )
  
  def create_lecture(
                    self, 
                    lecture_icon:ft.Icon,
                    lecture_text:str="text", 
                    description:str="text", 
                    amount_topics:int=0, 
                    amount_excercise:int=0,
                    amount_videos:int=0,
                    on_block_click=None) -> ft.Container:
    """
    Note 1: Recommended Icon size is the 30 - 35 mark.
    """


    def _on_hover(e):
      content.opacity = 0.5 if e.data else 1
      content.update()
    
    async def _on_click(e): # Made this async to support the async callback!
      if on_block_click != None:
        await on_block_click(e) # Await the callback execution

    content=ft.Container(
      width=360,
      height=240,
      border=ft.Border.all(2, ft.Colors.with_opacity(0.3, ft.Colors.GREEN_400)),
      bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
      border_radius=15,
      padding=15,
      animate_opacity=ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT_SINE),
      on_click=_on_click,
      on_hover=_on_hover,

      content=ft.Column(
        controls=[

          # Title
          ft.Row(
            controls=[
              lecture_icon,
              ft.Text(lecture_text, theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono", margin=ft.Margin.only(left=10))
            ]
          ),

          # Description
          ft.Text(description, theme_style=ft.TextThemeStyle.LABEL_SMALL, font_family="JetBrains Mono", margin=ft.Margin.only(left=10)),

          # Anchor bottom =====================
          ft.Container(expand=True),
          ft.Divider(thickness=0),
          # Anchor bottom =====================

          # Lecture Details
          ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            # margin=ft.Margin.only(left=70, right=70),
            controls=[
              ft.Column([
                ft.Icon(ft.Icons.LIBRARY_BOOKS, color=ft.Colors.GREEN_100, tooltip="Sub-Topics"),
                ft.Text("Sub-Topics", theme_style=ft.TextThemeStyle.LABEL_SMALL, size=13),
                ft.Text(amount_topics, theme_style=ft.TextThemeStyle.LABEL_MEDIUM, size=12),
              ], 
              horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
              spacing=0
              ),

              ft.Column([
                ft.Icon(ft.Icons.EDIT_DOCUMENT, color=ft.Colors.GREEN_100, tooltip="Excercises"),
                ft.Text("Exercise", theme_style=ft.TextThemeStyle.LABEL_SMALL, size=13),
                ft.Text(amount_excercise, theme_style=ft.TextThemeStyle.LABEL_MEDIUM, size=12),
              ], 
              horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
              spacing=0
              ),

              ft.Column([
                ft.Icon(ft.Icons.VIDEO_COLLECTION, color=ft.Colors.GREEN_100, tooltip="Videos"),
                ft.Text("Videos", theme_style=ft.TextThemeStyle.LABEL_SMALL, size=13),
                ft.Text(amount_videos, theme_style=ft.TextThemeStyle.LABEL_MEDIUM, size=12),
              ], 
              horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
              spacing=0,
              ),

            ]
          ),
        ]
      ), # End of content ----------------------------
    )

    return content