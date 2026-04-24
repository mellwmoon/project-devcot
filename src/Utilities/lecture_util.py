import flet as ft

class ItemLecture(ft.Row):

  def __init__(
              self, 
              text_label:str,
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
      main_content_container.bgcolor = ft.Colors(ft.Colors.GREEN_200) if not self.is_selected else ft.Colors(ON_HOVER_COLOR)
      self.is_selected = not self.is_selected

      if on_click is not None:
        on_click(e)

    def change_hover(e):
      if not self.is_selected:
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

class ContentLecture(ft.Column):

  def __init__(
              self,
              title:str="Title",
              description:str="Description",
              topics_amount:int=0,
              excercises_amount:int=0,
              videos_amount:int=0,
              topics_taken:float=0.0,
              excercises_taken:float=0.0,
              additional_controls:dict[ft.Icon, ft.Text]=None
              ):
    
    has_topics = False if topics_amount<=0 else True
    has_excercises = False if excercises_amount<=0 else True

    current_topics_ratio = topics_taken/(topics_amount if has_topics else 1)
    current_excercises_ratio = excercises_taken/(excercises_amount if has_excercises else 1)

    total_points = topics_amount + excercises_amount
    current_points = topics_taken + excercises_taken
    current_points_ratio = current_points / (total_points if total_points>0 else 1)

    super().__init__(
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Text(value=title, font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
        ft.Divider(),

        ft.Text(
          value=description,
          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
          text_align=ft.TextAlign.LEFT,
          font_family="Monospace",
          margin=ft.Margin.only(bottom=30)
        ),

        # ft.Text(value="Contents", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
        # ft.Divider(),

        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          expand=True,
          controls=[
            ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.GREEN_100),
            ft.Text(topics_amount if has_topics else "No", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
            ft.Text("Sub-topics", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
          ],
          opacity=1.0 if has_topics else 0.4
        ),

        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          expand=True,
          controls=[
            ft.Icon(ft.Icons.EDIT_DOCUMENT, color=ft.Colors.GREEN_100),
            ft.Text(excercises_amount if has_excercises else "No", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
            ft.Text("Excercises", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
          ],
          opacity=1.0 if has_excercises else 0.4
        ),

        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          expand=True,
          margin=ft.Margin.only(bottom=30),
          controls=[
            ft.Icon(ft.Icons.VIDEO_COLLECTION, color=ft.Colors.GREEN_100),
            ft.Text(str(videos_amount if videos_amount>0 else "No"), theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
            ft.Text("Videos", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
          ],
          opacity=1.0 if videos_amount>0 else 0.4
        ),

        # ft.Text(value="Your Progress", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
        # ft.Divider(),
        
        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          spacing=0,
          controls=[
            ft.ProgressBar(expand=True, value=current_points_ratio, color=ft.Colors.YELLOW),
            ft.Text(value=f"Overall Progress {current_points_ratio * 100:.2f}%", color=ft.Colors.YELLOW)
          ]
        ),

        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          expand=True,
          spacing=0,
          controls=[
            ft.ProgressBar(expand=True, value=current_excercises_ratio),
            ft.Text(f"Excercise Progress {current_excercises_ratio * 100:.2f}%")
          ]
        ),
        
        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          expand=True,
          spacing=0,
          controls=[
            ft.ProgressBar(expand=True, value=current_topics_ratio),
            ft.Text(f"Topics Progress {current_topics_ratio * 100:.2f}%")
          ]
        ),
      ]
    )
