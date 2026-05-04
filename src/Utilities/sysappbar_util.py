import flet as ft
import asyncio
import datetime
from Utilities import database_util as dubil

class SysAppBar(ft.AppBar):
    def __init__(self, page:ft.Page, topic_selected: str = "", is_appbar_only: bool = False, db:dubil.DatabaseManager=None):
        

        # ---------------------------------------------------
        # SETTINGS DIALOG UI SETUP
        # ---------------------------------------------------

        # 1. DatePicker (Matching web_signup.py style)
        self.settings_date_picker = ft.DatePicker(
            on_change=self.handle_date_change,
            first_date=datetime.datetime(1950, 1, 1),
            last_date=datetime.datetime(2026, 12, 31),
        )

        # 2. Dynamic Content Area (The right side of the popup)
        self.settings_content_area = ft.Container(expand=True)

        # 3. Sidebar Buttons
        # We store them in a list so we can easily loop through and change their colors when selected
        self.sidebar_buttons = [
            ft.TextButton("Account Info", data="account", on_click=self.handle_sidebar_click, style=self.get_sidebar_style(True)),
            ft.TextButton("Details & Scores", data="scores", on_click=self.handle_sidebar_click, style=self.get_sidebar_style(False)),
            ft.TextButton("Topics", data="topics", on_click=self.handle_sidebar_click, style=self.get_sidebar_style(False)),
        ]

        # 4. The Main Dialog Layout (700x350)
        self.settings_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("User Settings", font_family="JetBrains Mono"),
            content_padding=0, # Remove default padding so the sidebar touches the edges
            content=ft.Container(
                width=700,
                height=350,
                padding=ft.padding.only(left=20, top=20, right=20, bottom=10),
                content=ft.Row(
                    expand=True,
                    spacing=20,
                    controls=[
                        # Left Sidebar Column
                        ft.Column(
                            width=160,
                            controls=self.sidebar_buttons
                        ),
                        ft.VerticalDivider(width=1, color=ft.Colors.WHITE24),
                        # Right Content Area
                        self.settings_content_area
                    ]
                )
            ),
        )

        # Load the default view (Account Info) before opening
        self.load_account_view()

        # ---------------------------------------------------
        # ORIGINAL APPBAR SETUP
        # ---------------------------------------------------
        self.extramenu = [
            ft.PopupMenuItem(
                on_click=self.open_settings_dialog,
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
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=200,
                    opacity=0.4,
                ),
                disabled=True
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
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=200,
                    opacity=0.4,
                ),
                disabled=True
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
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=200,
                    opacity=0.4,
                ),
                disabled=True
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
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=170,
                    opacity=0.4,
                ),
                disabled=True
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
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=170,
                    opacity=0.4,
                ),
                disabled=True
            ),
        ]
        page.update()
        title_text = f"> DevCot: {topic_selected}" if not is_appbar_only else "> DevCot"
        
        super().__init__(
            title=ft.Text(
                value=title_text,
                font_family="JetBrains Mono",
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM
            ),
            leading_width=20,
            elevation=0,
            elevation_on_scroll=0,
            bgcolor=ft.Colors.BLACK_45,
            color=ft.Colors.GREEN_300,
            actions=[
                item_menus:=ft.PopupMenuButton(
                    margin=ft.Margin.only(right=20),
                    menu_padding=8,
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=self.extramenu
                )
            ]
        )
        self.item_menus = item_menus
        page.run_task(self._spot_instructor)

    # ---------------------------------------------------
    # INSTRUCTOR LOGIC (UNTOUCHED)
    # ---------------------------------------------------
    async def _spot_instructor(self) -> bool:
      r = await self.page.shared_preferences.get("current_user_type") == "instructor"
      print(r)
      await asyncio.sleep(0.1)
      if not r: return
      
      self.item_menus.items.append(ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),)
      self.item_menus.items.append(
          ft.PopupMenuItem(
          content=ft.Container(
              content=ft.Row(
                  spacing=20,
                  controls=[
                      ft.Icon(ft.Icons.HANDYMAN),
                      ft.Text(
                          value="Create a Lesson",
                          font_family="JetBrains Mono",
                          theme_style=ft.TextThemeStyle.LABEL_SMALL,
                      )
                  ]
              ),
              width=170,
              on_click=self.push_creator
          ),
        ),
      )
      self.item_menus.items.append(
          ft.PopupMenuItem(
          content=ft.Container(
              content=ft.Row(
                  spacing=20,
                  controls=[
                      ft.Icon(ft.Icons.EDIT_SQUARE),
                      ft.Text(
                          value="Go to Library",
                          font_family="JetBrains Mono",
                          theme_style=ft.TextThemeStyle.LABEL_SMALL,
                      )
                  ]
              ),
              width=170,
              on_click=self.push_library
          ),
        ),
      )
      self.update()
    
    async def push_creator(self, e):
      if self.page.route == "/creator":
        self.page.show_dialog(ft.SnackBar(ft.Text("You are Already there!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      elif self.page.route == "/lecture" or self.page.route == "/discussion":
        self.page.show_dialog(ft.SnackBar(ft.Text("Exit out of Lecture first.", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      await self.page.push_route("/creator")

    async def push_library(self, e):
      if self.page.route == "/library":
        self.page.show_dialog(ft.SnackBar(ft.Text("You are Already there!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      elif self.page.route == "/lecture" or self.page.route == "/discussion":
        self.page.show_dialog(ft.SnackBar(ft.Text("Exit out of Lecture first.", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      await self.page.push_route("/library")

    # ---------------------------------------------------
    # DIALOG HANDLERS & ROUTING
    # ---------------------------------------------------
    async def open_settings_dialog(self, e):
        self.page.show_dialog(self.settings_dialog)
        self.page.update()

    async def close_settings_dialog(self, e):
        self.settings_dialog.open = False
        self.page.update()

    # --- Sidebar Visuals ---
    def get_sidebar_style(self, is_selected: bool):
        """Returns the button style based on whether it is the currently active tab."""
        return ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            color=ft.Colors.GREEN_300 if is_selected else ft.Colors.WHITE54,
            bgcolor=ft.Colors.WHITE10 if is_selected else ft.Colors.TRANSPARENT,
            padding=ft.Padding.symmetric(horizontal=15, vertical=15),
            alignment=ft.Alignment.CENTER_LEFT
        )

    async def handle_sidebar_click(self, e):
        for btn in self.sidebar_buttons:
            btn.style = self.get_sidebar_style(btn.data == e.control.data)
        
        if e.control.data == "account":
            self.load_account_view()
        elif e.control.data == "scores":
            self.load_placeholder_view("Details & Scores", "Score history will appear here.")
        elif e.control.data == "topics":
            self.load_placeholder_view("Topics", "Topic preferences will appear here.")
            
        self.page.update()

    # ---------------------------------------------------
    # VIEW LOADERS (The Right Side Content)
    # ---------------------------------------------------
    def load_placeholder_view(self, title, description):
        """A generic view for tabs you haven't built out yet."""
        self.settings_content_area.content = ft.Column(
            expand=True,
            controls=[
                ft.Text(title, theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono", color=ft.Colors.GREEN_300),
                ft.Divider(color=ft.Colors.WHITE24),
                ft.Text(description, font_family="JetBrains Mono", color=ft.Colors.WHITE54)
            ]
        )

    def load_account_view(self):
        """Builds the main Account Information update form."""
        
        # UI Fields
        self.field_fname = ft.TextField(label="First Name", expand=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14), border_color=ft.Colors.WHITE24)
        self.field_lname = ft.TextField(label="Last Name", expand=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14), border_color=ft.Colors.WHITE24)
        self.field_pass = ft.TextField(expand=True,label="New Password", password=True, can_reveal_password=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14), border_color=ft.Colors.WHITE24)
        self.field_bdate = ft.TextField(
            label="Birthdate", 
            read_only=True, 
            on_click=lambda _: self.page.show_dialog(self.settings_date_picker),
            text_style=ft.TextStyle(font_family="JetBrains Mono", size=14),
            border_color=ft.Colors.WHITE24
        )

        self.settings_content_area.content = ft.Column(
           
            controls=[
                ft.Text("Personal Information", theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono", color=ft.Colors.GREEN_300),
                ft.Divider(color=ft.Colors.WHITE24),
                
                ft.Row([self.field_fname, self.field_lname]),
                
                self.field_pass,
                self.field_bdate,
                
                ft.Container(expand=True, margin=0, padding=0),

                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.TextButton("Discard", on_click=self.close_settings_dialog),
                        ft.FilledButton("Save Changes", on_click=self.save_account_changes, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700))
                    ]
                )
            ]
            
        )

    # ---------------------------------------------------
    # DATA HANDLING
    # ---------------------------------------------------
    def handle_date_change(self, e):
        """Updates the text field when the DatePicker is used."""
        if self.settings_date_picker.value:
            # Replicating the exact formatting from web_signup
            self.field_bdate.value = self.settings_date_picker.value.astimezone().strftime("%B %d, %Y")
            self.page.update()

    async def save_account_changes(self, e):
        """Fires when the Save Changes button is clicked."""
        print("--- Initiating Save ---")
        print(f"First Name: {self.field_fname.value}")
        print(f"Last Name: {self.field_lname.value}")
        print(f"Password: {self.field_pass.value}")
        print(f"Birthdate: {self.field_bdate.value}")
        
        # TODO: You will need to pass your 'db' manager into SysAppBar eventually 
        # to execute db.update_username(), db._update_single_field(password), etc.
        # Example:
        # new_username = f"{self.field_fname.value} {self.field_lname.value}"
        # db.update_username(current_user_id, new_username)
        
        self.page.show_dialog(ft.SnackBar(ft.Text("Settings saved successfully!", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800))
        await self.close_settings_dialog(e)