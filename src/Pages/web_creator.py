import flet as ft
import os
from Pages import web_lecture as wel
from Utilities import data_util
import json

class Creator(ft.View):
    def __init__(self):
        cur_appbar = wel.Lecture.load_appbar("Lecture Creator", is_appbar_only=True)

        self.current_loaded_file = None 

        self.lecture_data = {
            "title": "",
            "description": "",
            "icon": "MONITOR",
            "main_topics": [] 
        }

        self.tf_lecture_title = ft.TextField(label="Lecture Title", expand=True)
        self.tf_lecture_desc = ft.TextField(label="Description", expand=True, multiline=True)
        self.tf_lecture_icon = ft.TextField(label="Icon Name (e.g., MONITOR)", width=200)

        self.tf_main_topic = ft.TextField(label="New Main Topic Title", expand=True)
        self.dd_main_topics = ft.Dropdown(label="Target Main Topic", expand=True, options=[], on_select=self.dropdown_changed)
        
        self.tf_sub_topic = ft.TextField(label="New Sub-Topic Title", expand=True)
        self.dd_sub_topics = ft.Dropdown(label="Target Sub-Topic", expand=True, options=[], on_select=self.dropdown_changed)

        self.tf_markdown = ft.TextField(label="Markdown Content", multiline=True, min_lines=4, expand=True)
        
        self.tf_question = ft.TextField(label="Quiz Question", expand=True)
        self.quiz_options = [
            ft.TextField(label="Option 1 (Required)", expand=True),
            ft.TextField(label="Option 2 (Required)", expand=True),
            ft.TextField(label="Option 3 (Optional)", expand=True),
            ft.TextField(label="Option 4 (Optional)", expand=True)
        ]
        self.tf_answer_index = ft.TextField(label="Correct Option # (1-4)", width=200)

        # --- BROWSER MODAL ---
        self.browser_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.file_browser_dialog = ft.AlertDialog(
            title=ft.Text("Browse Local Curriculum Data", font_family="JetBrains Mono"),
            content=ft.Container(width=500, height=400, content=self.browser_content),
            actions=[ft.TextButton("Close", on_click=self.close_browser)]
        )

        # --- NEW: UNLOAD CONFIRMATION MODAL ---
        self.unload_dialog = ft.AlertDialog(
            title=ft.Text("Unload Lecture", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
            content=ft.Text("Do you want to save your changes before closing this lecture?", theme_style=ft.TextThemeStyle.LABEL_SMALL),
            actions=[
                ft.TextButton("Cancel", on_click=self.cancel_unload),
                ft.TextButton("Discard Changes", on_click=self.discard_unload, style=ft.ButtonStyle(color=ft.Colors.RED_400)),
                ft.FilledButton(content=ft.Text("Save & Unload"), on_click=self.save_and_unload)
            ]
        )

        # --- UI LAYOUT BLOCKS ---
        
        self.txt_mode = ft.Text("Mode: Creating New Lecture", color=ft.Colors.GREEN_300, font_family="JetBrains Mono", weight=ft.FontWeight.W_700)
        self.btn_delete = ft.FilledButton(content=ft.Text("Delete Lecture"), color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700, on_click=self.delete_lecture, visible=False)
        self.btn_unload = ft.FilledButton(content=ft.Text("Unload / Clear"), icon=ft.Icons.CLEAR_ALL, color=ft.Colors.WHITE, bgcolor=ft.Colors.ORANGE_700, on_click=self.request_unload, visible=False)
        
        # Your updated Column format!
        block_header = ft.Column([
            self.txt_mode,
            self.btn_delete,
            self.btn_unload,
            ft.FilledButton(content=ft.Text("Browse Lectures"), icon=ft.Icons.FOLDER_OPEN, on_click=self.open_browser)
        ])

        block_meta = ft.Column([
            ft.Text("1. Lecture Core Details", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono"),
            ft.Row([self.tf_lecture_title, self.tf_lecture_icon]),
            self.tf_lecture_desc,
        ])

        block_topics = ft.Column([
            ft.Text("2. Curriculum Structure", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono"),
            ft.Row([self.tf_main_topic, ft.FilledButton(content=ft.Text("Add Main Topic"), on_click=self.add_main_topic)]),
            self.dd_main_topics,
            ft.Divider(color=ft.Colors.WHITE24),
            ft.Row([self.tf_sub_topic, ft.FilledButton(content=ft.Text("Add Sub-Topic"), on_click=self.add_sub_topic)]),
            self.dd_sub_topics,
        ])

        block_pages = ft.Column([
            ft.Text("3. Inject Pages into Targeted Sub-Topic", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono"),
            ft.Text("Add Content Page", theme_style=ft.TextThemeStyle.LABEL_LARGE, color=ft.Colors.GREEN_300),
            self.tf_markdown,
            ft.FilledButton(content=ft.Text("Inject Markdown Page"), on_click=self.add_content_page),
            ft.Divider(color=ft.Colors.WHITE24),
            ft.Text("Add Quiz Page", theme_style=ft.TextThemeStyle.LABEL_LARGE, color=ft.Colors.GREEN_300),
            self.tf_question,
            ft.Row([self.quiz_options[0], self.quiz_options[1]]),
            ft.Row([self.quiz_options[2], self.quiz_options[3]]),
            ft.Row([self.tf_answer_index, ft.FilledButton(content=ft.Text("Inject Quiz Page"), on_click=self.add_quiz_page)]),
        ])

        block_save = ft.Column([
            ft.Divider(color=ft.Colors.WHITE24),
            txt_status := ft.Text("Ready.", color=ft.Colors.GREEN_300),
            ft.FilledButton(content=ft.Text("SAVE LECTURE TO DISK"), width=400, on_click=self.save_lecture)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.txt_status = txt_status

        # --- SIDEBAR & SPLIT LAYOUT ---
        self.sidebar_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)
        self.refresh_sidebar()

        sidebar_area = ft.Container(
            width=320,
            padding=15,
            border=ft.Border.all(1, ft.Colors.WHITE24),
            border_radius=10,
            height=500,
            content=self.sidebar_column
        )

        main_body = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=30,
            height=500, 
            controls=[block_header, ft.Divider(color=ft.Colors.WHITE24), block_meta, ft.Divider(color=ft.Colors.WHITE24), block_topics, ft.Divider(color=ft.Colors.WHITE24), block_pages, block_save]
        )

        main_creation_area = ft.Container(
            padding=20, expand=True,
            border=ft.Border.all(1, ft.Colors.WHITE24), border_radius=10,
            margin=ft.Margin.only(left=80, right=80), 
            content=main_body
        )

        content_area = ft.SafeArea(
            content=ft.Row(
                expand=True,
                spacing=20,
                margin=ft.Margin.only(left=20, right=20, top=20, bottom=20),
                controls=[sidebar_area, main_creation_area]
            )
        )

        super().__init__(
            route="/creator", appbar=cur_appbar,
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[content_area]
        )


    # --- NEW: FORM CLEARING LOGIC ---

    def clear_form(self):
        """Resets the UI back to a completely blank slate."""
        self.current_loaded_file = None
        self.lecture_data = {"title": "", "description": "", "icon": "MONITOR", "main_topics": []}
        
        self.tf_lecture_title.value = ""
        self.tf_lecture_desc.value = ""
        self.tf_lecture_icon.value = ""
        
        self.dd_main_topics.options.clear()
        self.dd_main_topics.value = None
        self.dd_sub_topics.options.clear()
        self.dd_sub_topics.value = None
        
        self.tf_markdown.value = ""
        self.tf_question.value = ""
        self.tf_answer_index.value = ""
        for opt in self.quiz_options: opt.value = ""

        self.txt_mode.value = "Mode: Creating New Lecture"
        self.txt_mode.color = ft.Colors.GREEN_300
        self.btn_delete.visible = False
        self.btn_unload.visible = False
        
        self.refresh_sidebar()

    # --- UNLOAD DIALOG HANDLERS ---

    def request_unload(self, e):
        e.page.show_dialog(self.unload_dialog)

    def cancel_unload(self, e):
        self.unload_dialog.open = False
        self.page.update()

    def discard_unload(self, e):
        self.unload_dialog.open = False
        self.clear_form()
        self.show_snack(e, "Changes discarded and form cleared.")
        self.page.update()

    def save_and_unload(self, e):
        self.unload_dialog.open = False
        self.save_lecture(e) # Calls your existing save logic
        self.clear_form()    # Then wipes the screen
        self.show_snack(e, "Lecture saved and unloaded successfully!")
        self.page.update()


    # --- IN-APP FILE BROWSER LOGIC ---

    def open_browser(self, e):
        self.browser_content.controls.clear()
        lectures = data_util.load_all_lectures()
        
        if not lectures:
            self.browser_content.controls.append(ft.Text("No saved lectures found in Data/lectures.", color=ft.Colors.WHITE54))
        else:
            for lec in lectures:
                self.browser_content.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.GREEN_300),
                        title=ft.Text(lec.get("title", "Untitled")),
                        subtitle=ft.Text(f"File: {lec.get('file_id')} | Topics: {lec.get('topics_amount', 0)}"),
                        on_click=lambda e, payload=lec: self.load_lecture_into_ui(e, payload)
                    )
                )

        self.page.show_dialog(self.file_browser_dialog)

    def close_browser(self, e):
        self.file_browser_dialog.open = False
        self.page.update()

    def load_lecture_into_ui(self, e, payload):
        self.close_browser(e)
        
        self.lecture_data = payload
        self.current_loaded_file = payload.get("file_id")

        self.tf_lecture_title.value = payload.get("title", "")
        self.tf_lecture_desc.value = payload.get("description", "")
        self.tf_lecture_icon.value = payload.get("icon", "MONITOR")

        self.dd_main_topics.options.clear()
        for mt in self.lecture_data.get("main_topics", []):
            self.dd_main_topics.options.append(ft.dropdown.Option(mt["topic_title"]))
            
        self.dd_main_topics.value = None
        self.dd_sub_topics.options.clear()
        self.dd_sub_topics.value = None

        self.txt_mode.value = f"Mode: Editing '{self.current_loaded_file}'"
        self.txt_mode.color = ft.Colors.YELLOW_300
        
        # Reveal both Delete and Unload buttons!
        self.btn_delete.visible = True
        self.btn_unload.visible = True

        self.refresh_sidebar()
        self.show_snack(e, f"Loaded {self.current_loaded_file} successfully!")

    def delete_lecture(self, e):
        if self.current_loaded_file:
            data_util.delete_lecture(self.current_loaded_file)
            self.clear_form() # Utilizing our new helper method!
            self.show_snack(e, "Lecture deleted permanently.")


    # --- SIDEBAR & HIGHLIGHT LOGIC ---

    def refresh_sidebar(self):
        self.sidebar_column.controls.clear()
        self.sidebar_column.controls.append(
            ft.Text("Curriculum Tree", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono")
        )
        
        if not self.lecture_data.get("main_topics"):
            self.sidebar_column.controls.append(ft.Text("No topics added yet.", color=ft.Colors.WHITE54))
            return

        for mt in self.lecture_data["main_topics"]:
            is_active_main = (self.dd_main_topics.value == mt['topic_title'])
            main_bg = ft.Colors.GREEN_800 if is_active_main else ft.Colors.TRANSPARENT
            main_border = ft.Colors.GREEN_400 if is_active_main else ft.Colors.WHITE24

            self.sidebar_column.controls.append(
                ft.Container(
                    content=ft.Text(f"Topic: {mt['topic_title']}", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                    bgcolor=main_bg, border=ft.Border.all(1, main_border), border_radius=6, padding=10,
                    on_click=lambda e, title=mt['topic_title']: self.sidebar_main_clicked(e, title)
                )
            )
            
            for st in mt.get("sub_topics", []):
                is_active_sub = is_active_main and (self.dd_sub_topics.value == st['sub_title'])
                sub_bg = ft.Colors.with_opacity(0.15, ft.Colors.YELLOW) if is_active_sub else ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
                sub_border = ft.Colors.YELLOW if is_active_sub else ft.Colors.WHITE24

                pages_count = sum(1 for p in st.get("pages", []) if p["type"] == "content")
                quiz_count = sum(1 for p in st.get("pages", []) if p["type"] == "quiz")
                
                row_controls = []
                if is_active_sub: row_controls.append(ft.Icon(ft.Icons.ARROW_RIGHT_ALT, color=ft.Colors.YELLOW, size=18))
                row_controls.append(ft.Text(f"{st['sub_title']}\n{pages_count} pages, {quiz_count} quizzes", size=12, color=ft.Colors.YELLOW if is_active_sub else ft.Colors.WHITE))

                self.sidebar_column.controls.append(
                    ft.Container(
                        content=ft.Row(row_controls, alignment=ft.MainAxisAlignment.START),
                        border=ft.Border.all(1, sub_border), bgcolor=sub_bg, border_radius=6,
                        padding=ft.Padding.only(left=10, right=10, top=5, bottom=5), margin=ft.Margin.only(left=20),
                        on_click=lambda e, m_title=mt['topic_title'], s_title=st['sub_title']: self.sidebar_sub_clicked(e, m_title, s_title)
                    )
                )
        try:
            self.update()
        except AssertionError:
            pass

    def dropdown_changed(self, e):
        if e.control == self.dd_main_topics:
            self.rebuild_sub_dropdown_options(self.dd_main_topics.value)
            self.dd_sub_topics.value = None
        self.refresh_sidebar()

    def sidebar_main_clicked(self, e, main_title):
        self.dd_main_topics.value = main_title
        self.rebuild_sub_dropdown_options(main_title)
        self.dd_sub_topics.value = None
        self.refresh_sidebar()

    def sidebar_sub_clicked(self, e, main_title, sub_title):
        self.dd_main_topics.value = main_title
        self.rebuild_sub_dropdown_options(main_title)
        self.dd_sub_topics.value = sub_title
        self.refresh_sidebar()

    def rebuild_sub_dropdown_options(self, target_main_title):
        self.dd_sub_topics.options.clear()
        for mt in self.lecture_data.get("main_topics", []):
            if mt["topic_title"] == target_main_title:
                for st in mt.get("sub_topics", []):
                    self.dd_sub_topics.options.append(ft.dropdown.Option(st["sub_title"]))
                break

    # --- DATA INJECTION LOGIC ---

    def add_main_topic(self, e):
        title = self.tf_main_topic.value.strip()
        if not title: return
        self.lecture_data["main_topics"].append({"topic_title": title, "sub_topics": []})
        self.dd_main_topics.options.append(ft.dropdown.Option(title))
        self.dd_main_topics.value = title 
        self.tf_main_topic.value = ""
        self.rebuild_sub_dropdown_options(title)
        self.dd_sub_topics.value = None
        self.refresh_sidebar()
        self.show_snack(e, f"Main Topic '{title}' created!")

    def add_sub_topic(self, e):
        main_target = self.dd_main_topics.value
        sub_title = self.tf_sub_topic.value.strip()
        if not main_target or not sub_title:
            self.show_snack(e, "Please select a Main Topic and enter a Sub-Topic title.")
            return
        for mt in self.lecture_data["main_topics"]:
            if mt["topic_title"] == main_target:
                mt["sub_topics"].append({"sub_title": sub_title, "pages": []})
                break
        self.dd_sub_topics.options.append(ft.dropdown.Option(sub_title))
        self.dd_sub_topics.value = sub_title 
        self.tf_sub_topic.value = ""
        self.refresh_sidebar()
        self.show_snack(e, f"Sub-Topic '{sub_title}' added to '{main_target}'!")

    def get_targeted_sub_topic(self):
        main_target = self.dd_main_topics.value
        sub_target = self.dd_sub_topics.value
        if not main_target or not sub_target: return None
        for mt in self.lecture_data["main_topics"]:
            if mt["topic_title"] == main_target:
                for st in mt.get("sub_topics", []):
                    if st["sub_title"] == sub_target:
                        return st.setdefault("pages", [])
        return None

    def add_content_page(self, e):
        target_pages = self.get_targeted_sub_topic()
        if target_pages is None:
            self.show_snack(e, "You must select a Sub-Topic to inject pages into!")
            return
        target_pages.append({"type": "content", "markdown": self.tf_markdown.value})
        self.tf_markdown.value = ""
        self.refresh_sidebar()
        self.show_snack(e, "Content Page Injected!")

    def add_quiz_page(self, e):
        target_pages = self.get_targeted_sub_topic()
        if target_pages is None:
            self.show_snack(e, "You must select a Sub-Topic to inject pages into!")
            return
        valid_options = [opt.value for opt in self.quiz_options if opt.value.strip() != ""]
        if len(valid_options) < 2:
            self.show_snack(e, "Quizzes need at least 2 options!")
            return
        try:
            correct_idx = int(self.tf_answer_index.value) - 1
            if correct_idx < 0 or correct_idx >= len(valid_options): raise ValueError
        except ValueError:
            self.show_snack(e, f"Answer must be a number between 1 and {len(valid_options)}")
            return
        target_pages.append({"type": "quiz", "question": self.tf_question.value, "options": valid_options, "correct_index": correct_idx})
        self.tf_question.value = ""
        self.tf_answer_index.value = ""
        for opt in self.quiz_options: opt.value = ""
        self.refresh_sidebar()
        self.show_snack(e, "Quiz Page Injected!")

    def save_lecture(self, e):
        self.lecture_data["title"] = self.tf_lecture_title.value
        self.lecture_data["description"] = self.tf_lecture_desc.value
        self.lecture_data["icon"] = self.tf_lecture_icon.value

        total_topics = 0
        total_exercises = 0
        for mt in self.lecture_data.get("main_topics", []):
            for st in mt.get("sub_topics", []):
                for page in st.get("pages", []):
                    if page["type"] == "content": total_topics += 1
                    elif page["type"] == "quiz": total_exercises += 1
                        
        self.lecture_data["topics_amount"] = total_topics
        self.lecture_data["exercises_amount"] = total_exercises
        self.lecture_data["videos_amount"] = 0

        file_name = self.lecture_data["title"].replace(" ", "_").lower()
        if not file_name: file_name = "untitled_lecture"
        
        if self.current_loaded_file and self.current_loaded_file != (file_name + ".json"):
            data_util.delete_lecture(self.current_loaded_file)

        data_util.save_lecture(file_name, self.lecture_data)
        
        self.current_loaded_file = file_name + ".json"
        self.txt_mode.value = f"Mode: Editing '{self.current_loaded_file}'"
        self.txt_mode.color = ft.Colors.YELLOW_300
        
        self.btn_delete.visible = True
        self.btn_unload.visible = True
        
        self.txt_status.value = f"SUCCESS: Saved '{file_name}.json' with {total_topics} content pages and {total_exercises} quizzes."
        self.update()

    def show_snack(self, e, text):
        e.page.snack_bar = ft.SnackBar(ft.Text(text))
        e.page.snack_bar.open = True
        self.update()