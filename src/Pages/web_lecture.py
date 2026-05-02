import flet as ft
from Utilities import lecture_util as lutil

# Note 1: content_lecture_list -> Main list container
# Note 2: container_desc -> Main Description container,
#         use lutil.ContentLecture to create details about lecture.

class Lecture(ft.View):
  def __init__(self, page: ft.Page):
    
    self.payload = page.session.store.get("current_lecture_payload")
    
    if not self.payload:
      self.payload = {"title": "Error", "description": "No payload found.", "main_topics": []}

    self.TOPIC_SELECTED = self.payload.get("title", "Unknown Lecture")
    
    cur_appbar = self.load_appbar(self.TOPIC_SELECTED)

    # State tracking variables for interactivity
    self.sub_topic_items = []
    self.target_discuss_pages = None

    # BODY =============================================

    container_list = ft.Container(
      width=450,
      padding=ft.Padding.only(left=10, right=10, top=5, bottom=5),
      border_radius=10,
      content=ft.Column(
        height=600,
        scroll=ft.ScrollMode.ADAPTIVE,
        controls=[ft.Container(
          border_radius=10,
          padding=ft.Padding.only(right=16),
          content=(content_lecture_list:=ft.Column(
            controls=[]
          ))
        )]
      )
    )

    self.container_desc = ft.Container(
      expand=True,
      padding=ft.Padding.only(left=20, right=20, top=15, bottom=15),
      border_radius=10,
      border=ft.Border.all(1.5, ft.Colors.GREEN_300),
      content=lutil.ContentLecture(
        title="Select a Topic",
        description=self.payload.get("description", "Choose a sub-topic from the left to view details."),
        topics_amount=0, excercises_amount=0, videos_amount=0, topics_taken=0, excercises_taken=0,
      )
    )

    btn_study = ft.FilledButton(
        margin=ft.Margin.only(top=15), height=50, width=230,
        content=ft.Text("Study ->", font_family="JetBrains Mono", weight=ft.FontWeight.W_700, size=18),
        on_click=self.go_study
    )
    
    btn_back = ft.OutlinedButton(
        margin=ft.Margin.only(top=6), height=50, width=150,
        content=ft.Text("Go Back", font_family="JetBrains Mono", weight=ft.FontWeight.W_700, size=18),
        on_click=self.go_back
    )

    body_content = ft.Row(
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      spacing=20,
      controls=[
        container_list,
        ft.Column(
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          expand=True, 
          controls=[self.container_desc, btn_study, btn_back]
        ),
      ]
    )

    # --- DYNAMIC GENERATION LOGIC ---
    self.generate_lecture_items(content_lecture_list)

    super().__init__(
      route="/lecture",
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[ft.SafeArea(content=body_content, margin=5)],
      appbar=cur_appbar
    )

  # --- INTERACTIVITY & LOGIC ---
  def generate_lecture_items(self, list_container):
      """Loops through the JSON payload and builds the UI using lutil components"""
      for mt in self.payload.get("main_topics", []):
          list_container.controls.append(lutil.ItemLecture(mt["topic_title"], is_heading=True))
          
          for st in mt.get("sub_topics", []):              
              def make_click_handler(item_ref, mt_data, st_data):
                  def handler(e):
                      self.on_subtopic_click(e, item_ref[0], mt_data, st_data)
                  return handler
              
              
              item_ref = [None] 
              
              new_sub_item = lutil.ItemLecture(
                  text_label=st["sub_title"], 
                  is_heading=False,
                  on_click=make_click_handler(item_ref, mt, st)
              )
              
              item_ref[0] = new_sub_item
              self.sub_topic_items.append(new_sub_item)
              list_container.controls.append(new_sub_item)

  def on_subtopic_click(self, e, clicked_item, parent_main_topic, sub_topic_data):
      """Handles the 'Radio Button' visual logic and updates the side panel"""
      
      for item in self.sub_topic_items:
          if item != clicked_item and item.is_selected:
              item.is_selected = False

      topics_amt = 0
      quizzes_amt = 0
      for st in parent_main_topic.get("sub_topics", []):
          for page in st.get("pages", []):
              if page["type"] == "content": topics_amt += 1
              if page["type"] == "quiz": quizzes_amt += 1

      self.container_desc.content = lutil.ContentLecture(
          title=parent_main_topic.get("topic_title", "Topic"),
          description=sub_topic_data.get('description'),
          topics_amount=topics_amt,
          excercises_amount=quizzes_amt,
          videos_amount=0, topics_taken=0, excercises_taken=0
      )
      self.container_desc.update()

      self.target_discuss_pages = sub_topic_data.get("pages", [])

  # --- ASYNC ROUTING ---
  async def go_study(self, e):
      if self.target_discuss_pages is not None:
          
          e.page.session.store.set("discuss_pages", self.target_discuss_pages)
          await self.page.push_route("/discuss")

      else:
          e.page.snack_bar = ft.SnackBar(ft.Text("Please select a sub-topic first!"))
          e.page.snack_bar.open = True
          e.page.update()

  async def go_back(self, e):
      await e.page.push_route("/library")

  @classmethod
  def load_appbar(self, topic_selected:str="", is_appbar_only=False):
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
      
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),

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
     
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),

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