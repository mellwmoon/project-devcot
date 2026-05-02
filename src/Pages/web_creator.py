import flet as ft
import os
from Pages import web_lecture as wel
from Utilities import data_util
import json

class Creator(ft.View):
    def __init__(self):
        cur_appbar = wel.Lecture.load_appbar("Lecture Creator", is_appbar_only=True)

        self.current_loaded_file = None 
        self._target_edit_main = None
        self._target_edit_sub = None
        
        # Tracking for the new Page Editor
        self._editing_page_index = None 

        self.lecture_data = {
            "title": "",
            "description": "",
            "icon": "MONITOR",
            "main_topics": [] 
        }

        # --- STANDARD INPUT FIELDS ---
        self.tf_lecture_title = ft.TextField(label="Lecture Title", expand=True)
        self.tf_lecture_desc = ft.TextField(label="Description", expand=True, multiline=True)
        self.tf_lecture_icon = ft.TextField(label="Icon Name (e.g., MONITOR)", width=200)

        self.tf_main_topic = ft.TextField(label="New Main Topic Title", expand=True)
        self.dd_main_topics = ft.Dropdown(label="Target Main Topic", expand=True, options=[], on_select=self.dropdown_changed)
        
        self.tf_sub_topic = ft.TextField(label="New Sub-Topic Title", expand=True)
        self.tf_sub_topic_desc = ft.TextField(label="Sub-Topic Description (Optional)", expand=True, multiline=True, min_lines=2)
        
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

        # --- NEW: PAGE EDITOR FIELDS ---
        self.edit_tf_markdown = ft.TextField(label="Edit Markdown", multiline=True, expand=True)
        self.edit_tf_question = ft.TextField(label="Edit Question")
        self.edit_quiz_options = [ft.TextField(label=f"Option {i+1}") for i in range(4)]
        self.edit_tf_answer_index = ft.TextField(label="Correct Option #", width=150)


        # --- MODALS (DIALOGS) ---
        self.browser_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.file_browser_dialog = ft.AlertDialog(
            title=ft.Text("Browse Local Curriculum Data", font_family="JetBrains Mono"),
            content=ft.Container(width=500, height=400, content=self.browser_content),
            actions=[ft.TextButton("Close", on_click=self.close_browser)]
        )

        self.unload_dialog = ft.AlertDialog(
            title=ft.Text("Unload Lecture", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
            content=ft.Text("Do you want to save your changes before closing this lecture?", theme_style=ft.TextThemeStyle.LABEL_SMALL),
            actions=[
                ft.TextButton("Cancel", on_click=self.cancel_unload),
                ft.TextButton("Discard Changes", on_click=self.discard_unload, style=ft.ButtonStyle(color=ft.Colors.RED_400)),
                ft.FilledButton(content=ft.Text("Save & Unload"), on_click=self.save_and_unload)
            ]
        )

        self.tf_quick_edit_title = ft.TextField(label="Sub-Topic Title")
        self.tf_quick_edit_desc = ft.TextField(label="Description", multiline=True, min_lines=2)
        
        self.edit_sub_dialog = ft.AlertDialog(
            title=ft.Text("Edit Sub-Topic", font_family="JetBrains Mono"),
            content=ft.Column([self.tf_quick_edit_title, self.tf_quick_edit_desc], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.close_quick_dialog(e, self.edit_sub_dialog)),
                ft.FilledButton("Save Changes", on_click=self.save_quick_edit)
            ]
        )
        
        self.delete_sub_dialog = ft.AlertDialog(
            title=ft.Text("Delete Sub-Topic", font_family="JetBrains Mono", color=ft.Colors.RED_400),
            content=ft.Text("Are you sure? This will permanently delete this sub-topic and all its associated pages.", theme_style=ft.TextThemeStyle.LABEL_SMALL),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.close_quick_dialog(e, self.delete_sub_dialog)),
                ft.FilledButton("Delete Permanently", on_click=self.confirm_quick_delete, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE))
            ]
        )

        # --- NEW: PAGE EDITOR MODAL ---
        self.editor_sidebar = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)
        self.editor_workspace = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
        
        self.page_editor_dialog = ft.AlertDialog(
            title=ft.Text("Manage Sub-Topic Pages", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
            content=ft.Container(
                width=750, height=450, 
                content=ft.Row([
                    # Left Sidebar for Page List
                    ft.Container(
                        width=220, border=ft.Border.all(1, ft.Colors.WHITE24), border_radius=8, 
                        padding=10, content=self.editor_sidebar
                    ),
                    # Right Workspace for Editing
                    ft.Container(
                        expand=True, border=ft.Border.all(1, ft.Colors.WHITE24), border_radius=8, 
                        padding=15, content=self.editor_workspace
                    )
                ])
            ),
            actions=[ft.FilledButton("Done", on_click=self.close_page_editor)]
        )

        # --- UI LAYOUT BLOCKS ---
        
        self.txt_mode = ft.Text("Mode: Creating New Lecture", color=ft.Colors.GREEN_300, font_family="JetBrains Mono", weight=ft.FontWeight.W_700)
        self.btn_delete = ft.FilledButton(content=ft.Text("Delete Lecture"), color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700, on_click=self.delete_lecture, visible=False)
        self.btn_unload = ft.FilledButton(content=ft.Text("Save and Unload/Clear"), icon=ft.Icons.CLEAR_ALL, color=ft.Colors.WHITE, bgcolor=ft.Colors.ORANGE_700, on_click=self.request_unload, visible=False)
        
        block_header = ft.Column([
            self.txt_mode,
            self.btn_delete,
            self.btn_unload,
            ft.FilledButton(content=ft.Text("Browse Lectures"), icon=ft.Icons.FOLDER_OPEN, on_click=self.open_browser)
        ])

        block_meta = ft.Column([
            ft.Text("Main Lecture Details", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono"),
            ft.Row([self.tf_lecture_title, self.tf_lecture_icon]),
            self.tf_lecture_desc,
        ])

        block_topics = ft.Column([
            ft.Text("Curriculum Structure", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono"),
            ft.Row([self.tf_main_topic, ft.FilledButton(content=ft.Text("Add Main Topic"), on_click=self.add_main_topic)]),
            self.dd_main_topics,
            ft.Divider(color=ft.Colors.WHITE24),
            ft.Column([
                ft.Row([self.tf_sub_topic, ft.FilledButton(content=ft.Text("Add Sub-Topic"), on_click=self.add_sub_topic)]),
                self.tf_sub_topic_desc 
            ]),
            self.dd_sub_topics,
        ])

        block_pages = ft.Column([
            ft.Row([
                ft.Text("Pages", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="JetBrains Mono", expand=True),
                ft.FilledButton("Manage Existing Pages", icon=ft.Icons.EDIT_DOCUMENT, on_click=self.open_page_editor) # NEW BUTTON
            ]),
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
            ft.FilledButton(content=ft.Text("SAVE LECTURE TO DISK"), width=400, height=40, on_click=self.save_lecture, bgcolor=ft.Colors.YELLOW_300)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.txt_status = txt_status

        # --- SIDEBAR & SPLIT LAYOUT ---
        self.sidebar_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)
        self.refresh_sidebar()

        sidebar_area = ft.Container(
            width=320, padding=15, border=ft.Border.all(1, ft.Colors.WHITE24),
            border_radius=10, height=500, content=self.sidebar_column
        )

        main_body = ft.Column(
            scroll=ft.ScrollMode.AUTO, spacing=30, height=500, 
            controls=[block_header, ft.Divider(color=ft.Colors.WHITE24), block_meta, ft.Divider(color=ft.Colors.WHITE24), block_topics, ft.Divider(color=ft.Colors.WHITE24), block_pages, block_save]
        )

        main_creation_area = ft.Container(
            padding=20, expand=True, border=ft.Border.all(1, ft.Colors.WHITE24), 
            border_radius=10, margin=ft.Margin.only(left=80, right=80), content=main_body
        )

        content_area = ft.SafeArea(
            content=ft.Row(
                expand=True, spacing=20, margin=ft.Margin.only(left=20, right=20, top=20, bottom=20),
                controls=[sidebar_area, main_creation_area]
            )
        )

        super().__init__(
            route="/creator", appbar=cur_appbar,
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[content_area]
        )

    # --- NEW: PAGE EDITOR LOGIC ---

    def open_page_editor(self, e):
        target_pages = self.get_targeted_sub_topic()
        if target_pages is None:
            self.show_snack(e, "You must select a Sub-Topic first!")
            return
            
        self.refresh_page_editor_sidebar()
        self.editor_workspace.controls.clear()
        self.editor_workspace.controls.append(ft.Text("Select a page from the left to edit.", color=ft.Colors.WHITE54))
        
        self.page.show_dialog(self.page_editor_dialog)

    def close_page_editor(self, e):
        self.page_editor_dialog.open = False
        self.refresh_sidebar() # Refresh main sidebar to update page counts if deleted
        self.page.update()

    def refresh_page_editor_sidebar(self):
        self.editor_sidebar.controls.clear()
        target_pages = self.get_targeted_sub_topic()
        
        if not target_pages:
            self.editor_sidebar.controls.append(ft.Text("No pages yet.", color=ft.Colors.WHITE54))
            return
            
        for i, page_data in enumerate(target_pages):
            icon = ft.Icons.DESCRIPTION if page_data["type"] == "content" else ft.Icons.QUIZ
            color = ft.Colors.GREEN_300 if page_data["type"] == "content" else ft.Colors.ORANGE_300
            
            self.editor_sidebar.controls.append(
                ft.Container(
                    content=ft.Row([ft.Icon(icon, color=color, size=16), ft.Text(f"Page {i+1}", size=12)]),
                    padding=10, border_radius=5, border=ft.Border.all(1, ft.Colors.WHITE24),
                    bgcolor=ft.Colors.with_opacity(0.1, color) if self._editing_page_index == i else ft.Colors.TRANSPARENT,
                    on_click=lambda e, index=i: self.load_page_into_workspace(index)
                )
            )

    def load_page_into_workspace(self, index):
        self._editing_page_index = index
        target_pages = self.get_targeted_sub_topic()
        page_data = target_pages[index]
        
        self.editor_workspace.controls.clear()
        
        if page_data["type"] == "content":
            self.edit_tf_markdown.value = page_data.get("markdown", "")
            self.editor_workspace.controls.extend([
                ft.Text(f"Editing Page {index+1} (Markdown)", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.Colors.GREEN_300),
                self.edit_tf_markdown
            ])
        elif page_data["type"] == "quiz":
            self.edit_tf_question.value = page_data.get("question", "")
            options = page_data.get("options", [])
            for i in range(4):
                self.edit_quiz_options[i].value = options[i] if i < len(options) else ""
            self.edit_tf_answer_index.value = str(page_data.get("correct_index", 0) + 1)
            
            self.editor_workspace.controls.extend([
                ft.Text(f"Editing Page {index+1} (Quiz)", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.Colors.ORANGE_300),
                self.edit_tf_question,
                ft.Row([self.edit_quiz_options[0], self.edit_quiz_options[1]]),
                ft.Row([self.edit_quiz_options[2], self.edit_quiz_options[3]]),
                self.edit_tf_answer_index
            ])
            
        # Add Save and Delete buttons
        self.editor_workspace.controls.append(
            ft.Row([
                ft.FilledButton("Save Page Changes", on_click=self.save_page_changes),
                ft.FilledButton("Delete Page", bgcolor=ft.Colors.RED_700, on_click=self.delete_page_changes)
            ], margin=ft.Margin.only(top=20))
        )
        
        self.refresh_page_editor_sidebar() # Updates the active highlight
        self.page.update()

    def save_page_changes(self, e):
        target_pages = self.get_targeted_sub_topic()
        page_data = target_pages[self._editing_page_index]
        
        if page_data["type"] == "content":
            page_data["markdown"] = self.edit_tf_markdown.value
        elif page_data["type"] == "quiz":
            valid_options = [opt.value for opt in self.edit_quiz_options if opt.value.strip() != ""]
            if len(valid_options) < 2:
                self.show_snack(e, "Quizzes need at least 2 options!")
                return
            try:
                correct_idx = int(self.edit_tf_answer_index.value) - 1
                if correct_idx < 0 or correct_idx >= len(valid_options): raise ValueError
            except ValueError:
                self.show_snack(e, f"Answer must be a number between 1 and {len(valid_options)}")
                return
                
            page_data["question"] = self.edit_tf_question.value
            page_data["options"] = valid_options
            page_data["correct_index"] = correct_idx
            
        self.show_snack(e, "Page updated successfully!")
        self.page.update()

    def delete_page_changes(self, e):
        target_pages = self.get_targeted_sub_topic()
        target_pages.pop(self._editing_page_index)
        
        self._editing_page_index = None
        self.editor_workspace.controls.clear()
        self.editor_workspace.controls.append(ft.Text("Page deleted. Select another page.", color=ft.Colors.WHITE54))
        
        self.refresh_page_editor_sidebar()
        self.show_snack(e, "Page removed from Sub-Topic.")
        self.page.update()


    # --- QUICK EDIT & DELETE LOGIC ---
    def close_quick_dialog(self, e, target_dialog):
        target_dialog.open = False
        self.page.update()

    def open_quick_edit(self, e, main_title, sub_title, sub_desc):
        self._target_edit_main = main_title
        self._target_edit_sub = sub_title
        self.tf_quick_edit_title.value = sub_title
        self.tf_quick_edit_desc.value = sub_desc
        self.page.show_dialog(self.edit_sub_dialog)

    def save_quick_edit(self, e):
        new_title = self.tf_quick_edit_title.value.strip()
        new_desc = self.tf_quick_edit_desc.value.strip()
        if not new_title: return

        for mt in self.lecture_data["main_topics"]:
            if mt["topic_title"] == self._target_edit_main:
                for st in mt.get("sub_topics", []):
                    if st["sub_title"] == self._target_edit_sub:
                        st["sub_title"] = new_title
                        st["description"] = new_desc
                        break

        if self.dd_main_topics.value == self._target_edit_main and self.dd_sub_topics.value == self._target_edit_sub:
            self.dd_sub_topics.value = new_title
            
        self.rebuild_sub_dropdown_options(self._target_edit_main)
        self.edit_sub_dialog.open = False
        self.refresh_sidebar()
        self.show_snack(e, "Sub-Topic updated!")
        self.page.update()

    def open_quick_delete(self, e, main_title, sub_title):
        self._target_edit_main = main_title
        self._target_edit_sub = sub_title
        self.page.show_dialog(self.delete_sub_dialog)

    def confirm_quick_delete(self, e):
        for mt in self.lecture_data["main_topics"]:
            if mt["topic_title"] == self._target_edit_main:
                mt["sub_topics"] = [st for st in mt.get("sub_topics", []) if st["sub_title"] != self._target_edit_sub]
                break

        if self.dd_main_topics.value == self._target_edit_main and self.dd_sub_topics.value == self._target_edit_sub:
            self.dd_sub_topics.value = None
            
        self.rebuild_sub_dropdown_options(self._target_edit_main)
        self.delete_sub_dialog.open = False
        self.refresh_sidebar()
        self.show_snack(e, "Sub-Topic deleted!")
        self.page.update()


    # --- FORM CLEARING LOGIC ---
    def clear_form(self):
        self.current_loaded_file = None
        self._target_edit_main = None
        self._target_edit_sub = None
        self.lecture_data = {"title": "", "description": "", "icon": "MONITOR", "main_topics": []}
        
        self.tf_lecture_title.value = ""
        self.tf_lecture_desc.value = ""
        self.tf_lecture_icon.value = ""
        self.dd_main_topics.options.clear()
        self.dd_main_topics.value = None
        self.dd_sub_topics.options.clear()
        self.dd_sub_topics.value = None
        
        self.tf_sub_topic.value = ""
        self.tf_sub_topic_desc.value = "" 
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
        self.page.show_dialog(self.unload_dialog)

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
        self.save_lecture(e) 
        self.clear_form()    
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
        
        self.btn_delete.visible = True
        self.btn_unload.visible = True

        self.refresh_sidebar()
        self.show_snack(e, f"Loaded {self.current_loaded_file} successfully!")

    def delete_lecture(self, e):
        if self.current_loaded_file:
            data_util.delete_lecture(self.current_loaded_file)
            self.clear_form() 
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
                
                sub_bg_normal = ft.Colors.with_opacity(0.15, ft.Colors.YELLOW) if is_active_sub else ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
                sub_bg_hover = ft.Colors.with_opacity(0.25, ft.Colors.YELLOW) if is_active_sub else ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
                sub_border = ft.Colors.YELLOW if is_active_sub else ft.Colors.WHITE24

                pages_count = sum(1 for p in st.get("pages", []) if p["type"] == "content")
                quiz_count = sum(1 for p in st.get("pages", []) if p["type"] == "quiz")
                
                row_controls = []
                if is_active_sub: row_controls.append(ft.Icon(ft.Icons.ARROW_RIGHT_ALT, color=ft.Colors.YELLOW, size=18))
                row_controls.append(ft.Text(f"{st['sub_title']}\n{pages_count} pages, {quiz_count} quizzes", size=12, color=ft.Colors.YELLOW if is_active_sub else ft.Colors.WHITE))

                action_row = ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.GREEN_300, icon_size=16, padding=0, width=24, height=24,
                                  on_click=lambda e, m=mt['topic_title'], s=st['sub_title'], d=st.get('description', ''): self.open_quick_edit(e, m, s, d)),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, icon_size=16, padding=0, width=24, height=24,
                                  on_click=lambda e, m=mt['topic_title'], s=st['sub_title']: self.open_quick_delete(e, m, s))
                ], spacing=0, visible=False)

                def make_hover_handler(bg_n, bg_h, actions):
                    def handler(e):
                        is_hovered = str(e.data).lower() == "true"
                        e.control.bgcolor = bg_h if is_hovered else bg_n
                        actions.visible = is_hovered
                        e.control.update()
                    return handler

                content_row = ft.Row([
                    ft.Row(row_controls, alignment=ft.MainAxisAlignment.START, expand=True), 
                    action_row 
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

                self.sidebar_column.controls.append(
                    ft.Container(
                        content=content_row,
                        border=ft.Border.all(1, sub_border), bgcolor=sub_bg_normal, border_radius=6,
                        padding=ft.Padding.only(left=10, right=10, top=5, bottom=5), margin=ft.Margin.only(left=20),
                        on_click=lambda e, m_title=mt['topic_title'], s_title=st['sub_title']: self.sidebar_sub_clicked(e, m_title, s_title),
                        on_hover=make_hover_handler(sub_bg_normal, sub_bg_hover, action_row)
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
        sub_desc = self.tf_sub_topic_desc.value.strip()
        if not sub_desc: sub_desc = "No description provided."

        if not main_target or not sub_title:
            self.show_snack(e, "Please select a Main Topic and enter a Sub-Topic title.")
            return
        
        for mt in self.lecture_data["main_topics"]:
            if mt["topic_title"] == main_target:
                mt["sub_topics"].append({"sub_title": sub_title, "description": sub_desc, "pages": []})
                break
                
        self.dd_sub_topics.options.append(ft.dropdown.Option(sub_title))
        self.dd_sub_topics.value = sub_title 
        
        self.tf_sub_topic.value = ""
        self.tf_sub_topic_desc.value = "" 
        
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