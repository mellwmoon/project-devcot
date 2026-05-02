import flet as ft

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
    
    # Initialize the base Row container
    super().__init__(vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, expand_loose=True)
    
    # Internal variables
    self._is_checked = is_checked
    self._is_heading = is_heading
    self._is_selected = is_selected
    self.on_click_callback = on_click
    self.text_label = text_label

    # --- MAIN TOPIC STYLE ---
    if self._is_heading:
        self.default_text = ft.Text(
            value=self.text_label,
            font_family="JetBrains Mono",
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.W_600,
            size=14
        )
        self.main_content_container = ft.Container(
            content=self.default_text,
            bgcolor=ft.Colors.TRANSPARENT,
            border=ft.Border.all(1, ft.Colors.WHITE24),
            border_radius=6,
            padding=10,
            expand=True
        )
        self.controls = [self.main_content_container]

    # --- SUB-TOPIC STYLE ---
    else:
        # The new Web Creator Arrow!
        self.arrow_icon = ft.Icon(ft.Icons.ARROW_RIGHT_ALT, color=ft.Colors.YELLOW, size=18, visible=False)
        
        # Kept the circle so students still know if they finished a topic
        self.check_icon = ft.Icon(
            icon=ft.Icons.CHECK_CIRCLE if self._is_checked else ft.Icons.CIRCLE_OUTLINED, 
            color=ft.Colors.GREEN_400 if self._is_checked else ft.Colors.WHITE54,
            size=15
        )

        self.default_text = ft.Text(
            value=self.text_label,
            font_family="JetBrains Mono",
            color=ft.Colors.WHITE,
            size=12
        )

        self.row_content = ft.Row(
            controls=[self.arrow_icon, self.check_icon, self.default_text],
            alignment=ft.MainAxisAlignment.START
        )

        self.main_content_container = ft.Container(
            content=self.row_content,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.WHITE24),
            border_radius=6,
            padding=ft.Padding.only(left=10, right=10, top=5, bottom=5),
            expand=True,
            on_click=self.on_click_container,
            on_hover=self.change_hover,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT_SINE)
        )

        self.controls = [
            ft.Container(width=20, expand_loose=True), # Indent block
            self.main_content_container
        ]

        # Force the initial visual state
        self.update_visual_state()

  # --- THE MAGIC FIX: SMART PROPERTIES ---
  @property
  def is_selected(self):
      return self._is_selected
      
  @is_selected.setter
  def is_selected(self, value):
      """When web_lecture changes this, update the UI automatically!"""
      self._is_selected = value
      self.update_visual_state()

  def update_visual_state(self):
      if self._is_heading:
          return # Headings are static in this view
          
      if self._is_selected:
          # Apply Yellow active state
          self.main_content_container.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.YELLOW)
          self.main_content_container.border = ft.Border.all(1, ft.Colors.YELLOW)
          self.default_text.color = ft.Colors.YELLOW
          self.arrow_icon.visible = True
      else:
          # Revert to White inactive state
          self.main_content_container.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
          self.main_content_container.border = ft.Border.all(1, ft.Colors.WHITE24)
          self.default_text.color = ft.Colors.WHITE
          self.arrow_icon.visible = False

      try:
          self.update()
      except Exception:
          pass # Prevents crashes if updated before being fully drawn

  # --- EVENT HANDLERS ---
  def on_click_container(self, e):
    self.is_selected = True # Triggers the setter and updates the color instantly!
    if self.on_click_callback is not None:
        self.on_click_callback(e)

  def change_hover(self, e):
    # Only apply hover effects if it isn't currently yellow/selected
    if not self._is_selected:
        is_hovered = str(e.data).lower() == "true"
        
        if is_hovered:
            self.main_content_container.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        else:
            self.main_content_container.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
            
        self.main_content_container.update()

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
      height=400,
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

        ft.Container(expand=True),
        ft.Text(value="Contents", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
        ft.Divider(),

        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          # expand=True,
          controls=[
            ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.GREEN_100),
            ft.Text(topics_amount if has_topics else "No", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
            ft.Text("Pages", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
          ],
          opacity=1.0 if has_topics else 0.4
        ),

        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          # expand=True,
          controls=[
            ft.Icon(ft.Icons.EDIT_DOCUMENT, color=ft.Colors.GREEN_100),
            ft.Text(excercises_amount if has_excercises else "No", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
            ft.Text("Excercises", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
          ],
          opacity=1.0 if has_excercises else 0.4
        ),

        ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          # expand=True,
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
          ],
          visible=False,
        ),


        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          expand=True,
          spacing=0,
          controls=[
            ft.ProgressBar(expand=True, value=current_excercises_ratio),
            ft.Text(f"Excercise Progress {current_excercises_ratio * 100:.2f}%")
          ],
          visible=False,
        ),

        
        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          expand=True,
          spacing=0,
          controls=[
            ft.ProgressBar(expand=True, value=current_topics_ratio),
            ft.Text(f"Topics Progress {current_topics_ratio * 100:.2f}%")
          ],
          visible=False,
        ),
      ]
    )
