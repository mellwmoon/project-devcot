import flet as ft
from rich import print
from Pages import web_lecture as wel
from Utilities import sysappbar_util as appbarutil
from Utilities import database_util as dubil
# Note 1: markdown_area is where actual lesson's content are built in.

class Discuss(ft.View):

  def __init__(self, page: ft.Page, db:dubil.DatabaseManager):
    self.client_page = page
    self.gdb = db
    self.pages_data = self.client_page.session.store.get("discuss_pages")
    
    # Fallback
    if not self.pages_data:
        self.pages_data = [{"type": "content", "markdown": "# No data loaded\nPlease go back and select a topic."}]

    self.current_page_index = 0
    self.current_score = 0
    # Tracking Progress in the Session (to feed back to web_lecture)
    # Currently almost useless ever since the progress bars have been removed
    if not page.session.store.get("user_progress"):
        page.session.store.set("user_progress", {"topics_taken": 0, "excercises_taken": 0})
    self.progress_tracker = page.session.store.get("user_progress")
    self.selected_topic = page.session.store.get("lecture_title")
    self.page_completed_flags = False * [self.current_page_index]

    cur_appbar = appbarutil.SysAppBar(page, self.selected_topic, db=db)

    # --- UI COMPONENTS ---
    
    self.dynamic_content_area = ft.Column(
        spacing=20,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        width=700,
    )

    self.btn_next = ft.FilledButton("Next", width=230, on_click=self.go_next)
    self.btn_prev = ft.Button("Previous", on_click=self.go_prev)
    self.btn_back = ft.Button("Back to list", on_click=self.go_back)

    # --- COMPLETION MODAL ---
    self.completion_dialog = ft.AlertDialog(
        title=ft.Text("Lesson Complete!", font_family="JetBrains Mono", color=ft.Colors.GREEN_300),
        content=ft.Text("You have reached the end of this sub-topic. Outstanding work!"),
        actions=[
            ft.TextButton("Review Lesson", on_click=self.close_dialog),
            ft.FilledButton("Return to Lecture Menu", on_click=self.go_back)
        ]
    )

    content_area = ft.SafeArea(
      margin=10,
      content=ft.Container(
        margin=ft.Margin.only(left=150, right=150, top=40, bottom=0),
        padding=10,
        height=540,
        border=ft.Border.all(1, ft.Colors.WHITE24), # Kept styling
        border_radius=10,
        content=ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.dynamic_content_area,
            ft.Divider(color=ft.Colors.WHITE24),
            self.btn_next,
            ft.Row(
              alignment=ft.MainAxisAlignment.CENTER,
              vertical_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[self.btn_back, self.btn_prev]
            )
          ]
        )
      )
    )

    self.lecture_markdown_style = ft.MarkdownStyleSheet(
        p_text_style=ft.TextStyle(
            font_family="Inter", 
            size=18,
            color=ft.Colors.GREEN_50,
            height=1.6
        ),

        h1_text_style=ft.TextStyle(
            font_family="Inter",
            size=32,
            weight=ft.FontWeight.W_800,
            color=ft.Colors.WHITE
        ),
        h2_text_style=ft.TextStyle(
            font_family="Inter",
            size=24,
            weight=ft.FontWeight.W_700,
            color=ft.Colors.WHITE
        ),
        h3_text_style=ft.TextStyle(
            font_family="Inter",
            size=20,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.WHITE70
        ),

        code_text_style=ft.TextStyle(
            font_family="JetBrains Mono",
            size=14,
            color=ft.Colors.BLUE_200,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_200),
        ),

        blockquote_decoration=ft.BoxDecoration(
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border=ft.Border(
                left=ft.BorderSide(4, ft.Colors.BLUE_400)
            ),
            border_radius=ft.border_radius.only(top_right=10, bottom_right=10)
        ),
        blockquote_padding=ft.Padding(left=16, top=10, right=16, bottom=10),
        blockquote_text_style=ft.TextStyle(
            font_family="Inter",
            size=16,
            color=ft.Colors.WHITE60,
            italic=True,
            height=1.5
        ),

        # --- Links ---
        a_text_style=ft.TextStyle(
            font_family="Inter",
            color=ft.Colors.BLUE_400,
            weight=ft.FontWeight.W_500,
            decoration=ft.TextDecoration.UNDERLINE
        ),

        # --- Lists ---
        # Ensures bullet points match the paragraph text perfectly
        list_bullet_text_style=ft.TextStyle(
            font_family="Inter",
            size=16,
            color=ft.Colors.WHITE70,
            height=1.6
        ),
    )

    super().__init__(
      route="/discuss",
      appbar=cur_appbar,
      controls=[content_area]
    )

    self.render_current_page()


  # --- STATE MACHINE LOGIC ---

  def render_current_page(self):
      self.dynamic_content_area.controls.clear()
      current_data = self.pages_data[self.current_page_index]

      if current_data["type"] == "content":
          # standard markdown
          md = ft.Markdown(current_data["markdown"], md_style_sheet=self.lecture_markdown_style, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,)
          self.dynamic_content_area.controls.append(md)
          
        #   if not self.page_completed_flags[self.current_page_index]:
        #       self.page_completed_flags[self.current_page_index] = True
            #   self.client_page.session.store.set("user_progress", self.progress_tracker)

      elif current_data["type"] == "quiz":
          # the Quiz UI
          question_text = ft.Text(current_data["question"], theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono")
          
          radio_options = []
          for i, opt in enumerate(current_data["options"]):
              radio_options.append(ft.Radio(value=str(i), label=opt))
          
          self.quiz_radiogroup = ft.RadioGroup(content=ft.Column(radio_options))
          
          btn_check = ft.FilledButton(
              content=ft.Text("Check Answer"), 
              on_click=lambda e: self.check_answer(e, current_data["correct_index"])
          )
          
          self.quiz_feedback = ft.Text("", font_family="JetBrains Mono")

          self.dynamic_content_area.controls.extend([
              question_text, 
              ft.Container(height=10),
              self.quiz_radiogroup, 
              ft.Container(height=10),
              btn_check, 
              self.quiz_feedback
          ])

      # Button States
      self.btn_prev.disabled = (self.current_page_index == 0)
      
      if self.current_page_index == len(self.pages_data) - 1:
          self.btn_next.content = ft.Text("Finish Sub-Topic")
      else:
          self.btn_next.content = ft.Text("Next Page")
      
      try:
          self.update()
      except Exception:
          pass

  # --- QUIZ LOGIC ---
  def check_answer(self, e, correct_index):
      user_choice = self.quiz_radiogroup.value
      
      if user_choice is None:
          self.quiz_feedback.value = "Please select an answer first."
          self.quiz_feedback.color = ft.Colors.ORANGE_400
      elif int(user_choice) == correct_index:
          self.current_score += 1
          self.quiz_feedback.value = "Correct! Excellent job."
          self.quiz_feedback.color = ft.Colors.GREEN_400
          
          # Log progress on correct answer!
          if not self.page_completed_flags[self.current_page_index]:
              self.progress_tracker["excercises_taken"] += 1
              self.page_completed_flags[self.current_page_index] = True
              e.page.session.store.set("user_progress", self.progress_tracker)
      else:
          self.quiz_feedback.value = "Incorrect. Take a moment to review and try again!"
          self.quiz_feedback.color = ft.Colors.RED_400
          
      self.update()


  # --- ASYNC ROUTING & NAVIGATION ---

  async def go_next(self, e):
      if self.current_page_index < len(self.pages_data) - 1:
          self.current_page_index += 1
          self.render_current_page()
      else:
          usr=await self.client_page.shared_preferences.get("current_user")
          e.page.show_dialog(self.completion_dialog)
          print(f"[bold][USER EVENT][/bold] [bold yellow]{usr}[/bold yellow] finished a part of [bold cyan]{self.selected_topic}[/bold cyan]")
          print(f"[bold][USER EVENT][/bold] [bold yellow]{usr}[/bold yellow] attained score of [bold cyan]{self.current_score}[/bold cyan]")
          print(f"[bold][SYS DATABASE][/bold] trying to save to database...")
          print("\n================================")
          self.gdb.connect()
          self.gdb.add_lesson(usr, self.selected_topic)
          self.gdb.add_lesson_score(usr, self.selected_topic, self.current_score)
          n=self.gdb.get_user_scores(usr)[self.selected_topic]
          self.gdb.close()
          print("=================================\n")
          print(f"[bold][SYS DATABASE][/bold] Stored as [bold yellow]{self.selected_topic} : {n}[/bold yellow]")
        #   self.progress_tracker["topics_taken"] += 1

  async def go_prev(self, e):
      if self.current_page_index > 0:
          self.current_page_index -= 1
          self.render_current_page()

  async def go_back(self, e):
      if self.completion_dialog.open:
          self.completion_dialog.open = False
          e.page.update()
          
      await e.page.push_route("/lecture")

  def close_dialog(self, e):
      self.completion_dialog.open = False
      e.page.update()