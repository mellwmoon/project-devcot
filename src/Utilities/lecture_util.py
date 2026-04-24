import flet as ft

class Item_Lecture(ft.Row):

  def __init__(
              self, 
              text_label:str,
              inner_spacing:int=20,
              is_heading=True,
              is_checked=False,
              is_selected=False,
              on_click=None
              ):
    
    self.is_checked = is_checked
    self.is_heading = is_heading
    self.is_selected = is_selected

    ON_HOVER_COLOR = ft.Colors.GREEN_400
    OFF_HOVER_COLOR = None
    COLOR_FADE_DURATION = 100

    hover_icon = ft.Icon(
      icon=ft.Icons.CIRCLE_OUTLINED if is_checked == False else ft.Icons.CHECK_CIRCLE, 
      color=ft.Colors.BLACK_87,
      size=25 if is_heading else 15
    )
    unhover_icon = ft.Icon(
      icon=ft.Icons.CIRCLE_OUTLINED if is_checked == False else ft.Icons.CHECK_CIRCLE, 
      color=ft.Colors.GREEN_300 if is_heading else ft.Colors.WHITE_24,
      size=25 if is_heading else 15
    )
    icon_anim = ft.AnimatedSwitcher(
      content=unhover_icon, 
      duration=COLOR_FADE_DURATION
    )

    hover_text = ft.Text(
      value=text_label,
      font_family="JetBrains Mono",
      color=ft.Colors.BLACK_87,
      theme_style=ft.TextThemeStyle.LABEL_MEDIUM if is_heading else ft.TextThemeStyle.LABEL_SMALL
    )
    unhover_text = ft.Text(
      value=text_label,
      font_family="JetBrains Mono",
      color=ft.Colors.GREEN_300 if is_heading else ft.Colors.WHITE_24,
      theme_style=ft.TextThemeStyle.LABEL_MEDIUM if is_heading else ft.TextThemeStyle.LABEL_SMALL
    )
    text_anim = ft.AnimatedSwitcher(
      content=unhover_text,
      duration=COLOR_FADE_DURATION
    )

    def on_click_container(e):
      main_content_container.border = ft.Border.all(width=1.3, color=ft.Colors.GREEN_300) if not self.is_selected else None
      self.is_selected = not self.is_selected

      if on_click is not None:
        on_click(e)

    def change_hover(e):
      main_content_container.bgcolor = ft.Colors(ON_HOVER_COLOR) if e.data == True else OFF_HOVER_COLOR
      icon_anim.content = hover_icon if e.data == True else unhover_icon
      text_anim.content = hover_text if e.data == True else unhover_text
      # icon.color = ON_HOVER_ICON_COLOR if e.data == True else OFF_HOVER_ICON_COLOR
      # btn_text.color = ON_HOVER_TEXT_COLOR if e.data == True else None

    main_content_container = ft.Container(
      content=ft.Row(
        controls=[icon_anim, text_anim]
      ),
      animate=ft.Animation(COLOR_FADE_DURATION, ft.AnimationCurve.EASE_IN_OUT_SINE),
      height=55 if is_heading else 40,
      padding=10,
      border_radius=4,
      expand=True,
      on_hover=change_hover,
      on_click=on_click_container
    )

    super().__init__(
      controls=[
        ft.Container(
          width=0 if is_heading else 30,
          # border=ft.Border.all(1, ft.Colors.WHITE_24),
          expand_loose=True,
        ),
        main_content_container
      ],
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=0,
      expand_loose=True,
    )