import flet as ft

class Item_Lecture(ft.Container):

  def __init__(
              self, 
              text_label:str,
              inner_spacing:int=20,
              is_heading=True,
              is_checked=False,
              is_selected=False,
              ):
    

    ON_HOVER_COLOR = ft.Colors.GREEN_400
    OFF_HOVER_COLOR = None
    COLOR_FADE_DURATION = 100

    hover_icon = ft.Icon(
      icon=ft.Icons.CIRCLE_OUTLINED, 
      color=ft.Colors.BLACK_87,
      size=25 if is_heading == True else 15
    )
    unhover_icon = ft.Icon(
      icon=ft.Icons.CIRCLE_OUTLINED, 
      color=ft.Colors.GREEN_300 if is_heading == True else ft.Colors.WHITE_24,
      size=25 if is_heading == True else 15
    )
    icon_anim = ft.AnimatedSwitcher(
      content=unhover_icon, 
      duration=COLOR_FADE_DURATION
    )

    hover_text = ft.Text(
      value=text_label,
      font_family="JetBrains Mono",
      color=ft.Colors.BLACK_87,
      theme_style=ft.TextThemeStyle.LABEL_MEDIUM if is_heading == True else ft.TextThemeStyle.LABEL_SMALL
    )
    unhover_text = ft.Text(
      value=text_label,
      font_family="JetBrains Mono",
      color=ft.Colors.GREEN_300 if is_heading == True else ft.Colors.WHITE_24,
      theme_style=ft.TextThemeStyle.LABEL_MEDIUM if is_heading == True else ft.TextThemeStyle.LABEL_SMALL
    )
    text_anim = ft.AnimatedSwitcher(
      content=unhover_text,
      duration=COLOR_FADE_DURATION
    )

    def change_hover(e):
      self.bgcolor = ft.Colors(ON_HOVER_COLOR) if e.data == True else OFF_HOVER_COLOR
      icon_anim.content = hover_icon if e.data == True else unhover_icon
      text_anim.content = hover_text if e.data == True else unhover_text
      # icon.color = ON_HOVER_ICON_COLOR if e.data == True else OFF_HOVER_ICON_COLOR
      # btn_text.color = ON_HOVER_TEXT_COLOR if e.data == True else None

    super().__init__(
      content=ft.Row(
        spacing=inner_spacing,
        controls=[icon_anim, text_anim],
        expand_loose=True,
      ),
      on_hover=change_hover,
      animate=ft.Animation(COLOR_FADE_DURATION, ft.AnimationCurve.EASE_IN_OUT_SINE),
      height=55 if is_heading == True else 38,
      padding=10,
      border_radius=4,
    )